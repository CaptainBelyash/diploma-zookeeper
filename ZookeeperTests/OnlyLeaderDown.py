import time

import numpy as np
import matplotlib.pyplot as plt

from blockade.BlockadeClient import BlockadeClient
from blockade.BlockadeContainer import get_zookeeper_blockade_container
from zookeeper.ZookeeperCluster import BlockadeZookeeperCluster
from zookeeper.ZookeeperMonitor.ZookeeperMonitor import Monitor
from zookeeper.ZookeeperMonitor.ZookeeperStatus import NodeMode

base_test_name = 'betaZkTestOnlyLeaderDown'


def only_leader_down_test():
    counts = range(3, 10)
    result = np.array([test_drop_leader(count) for count in counts])
    print(result)
    plt.plot(counts, result)
    plt.xlabel('node counts')
    plt.ylabel('median election time by 3 tests')
    plt.show()

def test_drop_leader(servers_count):
    elections_time = []

    zookeeper_cluster = BlockadeZookeeperCluster(servers_count)
    blockade_containers = [get_zookeeper_blockade_container(server) for server in zookeeper_cluster.servers]

    blockade = BlockadeClient(f"{base_test_name}{servers_count}", "localhost", 5000)

    monitor = Monitor(zookeeper_cluster.servers)

    try:
        for _ in range(3):
            try:
                blockade.start_new_blockade(blockade_containers)
                print(blockade.get_blockade())
                monitor.reset_stat()
                statuses = monitor.get_mntr_for_all_containers()
                leader = None
                for container in statuses:
                    if statuses[container].mode == NodeMode.LEADER:
                        leader = container

                leader, followers = make_partition([server.container_name for server in zookeeper_cluster.servers],
                                                   [leader])
                blockade.new_partition([leader, followers])

                # отслеживать конец выборов раз в 0.5 секунды например
                time.sleep(5)
                statuses = monitor.get_mntr_for_all_containers()

                election_time = np.array(list(map(float, [statuses[follower].election_time.avg for follower in followers])))
                elections_time.append(election_time)
            finally:
                blockade.return_to_normal(blockade_containers)
    finally:
        blockade.destroy_blockade()
    print(elections_time)
    print(np.median(elections_time, axis=1))
    print(np.mean(np.median(elections_time, axis=1)))
    return np.median(np.median(elections_time, axis=1))


def make_partition(original, first_part):
    second_part = original
    for container in first_part:
        second_part.remove(container)
    return [first_part, second_part]
