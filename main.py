import time

from blockade.BlockadeContainer import get_zookeeper_blockade_container
from blockade.BlockadeEnums import BlockadeVariables, NetworkState, BlockadeAction
from blockade.BlockadeClient import BlockadeClient
from zookeeper.ZookeeperCluster import BlockadeZookeeperCluster

client = BlockadeClient("zoopark", "localhost", 5000)


def main():
    zookeeper_blockade_cluster = BlockadeZookeeperCluster(3)

    blockade_containers = [get_zookeeper_blockade_container(server) for server in zookeeper_blockade_cluster.servers]

    client.start_new_blockade(blockade_containers)

    print(client.get_blockade())

    client.new_partition([["zoo3"], ["zoo2", "zoo1"]])

    print(client.get_blockade())
    client.delete_blockade()


if __name__ == '__main__':
    main()
