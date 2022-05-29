import requests

from blockade.BlockadeEnums import BlockadeVariables


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
        self.url = f"http://{address}:{port}/blockade"

    def get_all_blockades(self):
        request = requests.get(self.url)
        return request.json()

    def get_blockade(self):
        request = requests.get(f'{self.url}/{self.blockade_name}')
        return request.json()

    def start_new_blockade(self, containers):
        p = {"containers": {
                          container[BlockadeVariables.HOSTNAME]: container for container in containers
                      }}
        requests.post(f'{self.url}/{self.blockade_name}',
                      json=p)

    def delete_blockade(self):
        requests.delete(f'{self.url}/blockade/{self.blockade_name}')

    def new_partition(self, partitions):
        self.remove_all_partitions()
        self.add_partition(partitions)

    def add_partition(self, partitions):
        requests.post(f'{self.url}/{self.blockade_name}/partitions',
                      json={"partitions": partitions})

    def remove_all_partitions(self):
        requests.delete(f'{self.url}/{self.blockade_name}/partitions')

    def change_network_state(self, container_names, network_state):
        requests.post(f'{self.url}/{self.blockade_name}/network_state',
                      json={
                          "network_state": network_state,
                          "container_names": container_names
                      })

    def execute_action(self, container_names, action):
        requests.post(f'{self.url}/{self.blockade_name}/action',
                      json={
                          "command": action,
                          "container_names": container_names
                      })

    def get_chaos_status(self):
        request = requests.get(f'{self.url}/{self.blockade_name}/chaos')
        return request.json()["state"]

    def start_chaos(self, min_start_delay, max_start_delay, min_run_time, max_run_time,
                    min_containers_at_once, max_containers_at_once, events):
        requests.post(f'{self.url}/{self.blockade_name}/chaos',
                      json=get_chaos_params(min_start_delay, max_start_delay,
                                            min_run_time, max_run_time,
                                            min_containers_at_once, max_containers_at_once,
                                            events))

    def update_chaos(self, min_start_delay, max_start_delay, min_run_time, max_run_time,
                     min_containers_at_once, max_containers_at_once, events):
        requests.put(f'{self.url}/{self.blockade_name}/chaos',
                     json=get_chaos_params(min_start_delay, max_start_delay,
                                           min_run_time, max_run_time,
                                           min_containers_at_once, max_containers_at_once,
                                           events))

    def stop_chaos(self):
        requests.delete(f'{self.url}/{self.blockade_name}/chaos')
