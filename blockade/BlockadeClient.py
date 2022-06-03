import requests
from blockade.BlockadeEnums import BlockadeVariables, BlockadeAction, NetworkState


def get_chaos_params(min_start_delay, max_start_delay, min_run_time, max_run_time,
                     min_containers_at_once, max_containers_at_once, events):
    return {
        "min_start_delay": min_start_delay,
        "max_start_delay": max_start_delay,
        "min_run_time": min_run_time,
        "max_run_time": max_run_time,
        "min_containers_at_once": min_containers_at_once,
        "max_containers_at_once": max_containers_at_once,
        "events": events
    }


class BlockadeClient:
    def __init__(self, blockade_name, address, port):
        self.blockade_name = blockade_name
        self.baseUrl = f"http://{address}:{port}/blockade"
        self.containers = None

    def get_all_blockades(self):
        request = requests.get(self.baseUrl)
        return request.json()

    def get_blockade(self):
        response = requests.get(f'{self.baseUrl}/{self.blockade_name}')
        return response.json()

    def start_new_blockade(self, containers):
        self.create_new_blockade(containers)
        self.return_to_normal(containers)

    def return_to_normal(self, containers):
        self.stop_chaos()
        self.execute_action([container[BlockadeVariables.HOSTNAME] for container in containers], BlockadeAction.START)
        self.remove_all_partitions()
        self.change_network_state([container[BlockadeVariables.HOSTNAME] for container in containers],
                                  NetworkState.FAST)

    def destroy_blockade(self):
        self.execute_action([container for container in self.containers['containers'].keys()], BlockadeAction.KILL)

        self.delete_blockade()

    def create_new_blockade(self, containers):
        self.containers = {"containers": {
            container[BlockadeVariables.HOSTNAME]: container for container in containers
        }}

        response = requests.post(f'{self.baseUrl}/{self.blockade_name}', json=self.containers)

    def delete_blockade(self):
        requests.delete(f'{self.baseUrl}/blockade/{self.blockade_name}')

    def new_partition(self, partitions):
        self.remove_all_partitions()
        self.add_partition(partitions)

    def add_partition(self, partitions):
        print(partitions)
        requests.post(f'{self.baseUrl}/{self.blockade_name}/partitions',
                      json={"partitions": partitions})

    def remove_all_partitions(self):
        requests.delete(f'{self.baseUrl}/{self.blockade_name}/partitions')

    def change_network_state(self, container_names, network_state):
        requests.post(f'{self.baseUrl}/{self.blockade_name}/network_state',
                      json={
                          "network_state": network_state,
                          "container_names": container_names
                      })

    def execute_action(self, container_names, action):
        requests.post(f'{self.baseUrl}/{self.blockade_name}/action',
                      json={
                          "command": action,
                          "container_names": container_names
                      })

    def get_chaos_status(self):
        request = requests.get(f'{self.baseUrl}/{self.blockade_name}/chaos')
        return request.json()["state"]

    def start_chaos(self, min_start_delay, max_start_delay, min_run_time, max_run_time,
                    min_containers_at_once, max_containers_at_once, events):
        requests.post(f'{self.baseUrl}/{self.blockade_name}/chaos',
                      json=get_chaos_params(min_start_delay, max_start_delay,
                                            min_run_time, max_run_time,
                                            min_containers_at_once, max_containers_at_once,
                                            events))

    def update_chaos(self, min_start_delay, max_start_delay, min_run_time, max_run_time,
                     min_containers_at_once, max_containers_at_once, events):
        requests.put(f'{self.baseUrl}/{self.blockade_name}/chaos',
                     json=get_chaos_params(min_start_delay, max_start_delay,
                                           min_run_time, max_run_time,
                                           min_containers_at_once, max_containers_at_once,
                                           events))

    def stop_chaos(self):
        requests.delete(f'{self.baseUrl}/{self.blockade_name}/chaos')
