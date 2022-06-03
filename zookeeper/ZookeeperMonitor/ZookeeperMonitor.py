import os

from zookeeper.ZookeeperMonitor.ZookeeperStatus import ZookeeperStatus, Metric


class Monitor:
    def __init__(self, containers):
        self.containers = containers

    def reset_stat(self):
        for container in self.containers:
            os.system(f"echo srst | nc {container.address} {container.port}")

    def get_mntr_for_all_containers(self):
        containers_status = {}
        for container in self.containers:
            containers_status[container.container_name] = self.get_mntr(container)
        return containers_status

    def get_mntr(self, container):
        lines = []
        while len(lines) == 0:
            with os.popen(f"echo mntr | nc {container.address} {container.port}") as pipe:
                lines = pipe.readlines()
                if len(lines) == 0:
                    print('unexpected mntr empty result. retry...')
                    continue
                if 'This ZooKeeper instance is not currently serving requests' in lines[0]:
                    return ZookeeperStatus()
                extracted_data = {}
                for line in lines:
                    if '\t' in line:
                        splitted = line.split('\t')
                        extracted_data[splitted[0]] = splitted[1].rstrip('\n')
                    else:
                        print(f'unexpected line in monitor - {line}')
                return ZookeeperStatus(
                    mode=extracted_data['zk_server_state'],
                    unavailable_time=self.__get_metric(extracted_data, 'unavailable_time'),
                    election_time=self.__get_metric(extracted_data, 'election_time'))

    @staticmethod
    def __get_metric(extracted_data, metric_postfix):
        return Metric(
            avg_t=extracted_data[f'zk_avg_{metric_postfix}'],
            min_t=extracted_data[f'zk_min_{metric_postfix}'],
            max_t=extracted_data[f'zk_max_{metric_postfix}'],
            count=extracted_data[f'zk_cnt_{metric_postfix}'],
            sum_t=extracted_data[f'zk_sum_{metric_postfix}']
        )
