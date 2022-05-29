from zookeeper.ZookeeperContainer import ZookeeperContainerData


class BlockadeZookeeperCluster:
    def __init__(self, servers_count):
        self.first_container_port = 2181
        self.blockade_network_prefix = '172.17.0.'
        self.servers = self.__generate_servers(servers_count)
        self.__link_all_servers()

    def __generate_servers(self, servers_count):
        return [ZookeeperContainerData(i + 1,
                                       f'{self.blockade_network_prefix}{i + 2}',
                                       self.first_container_port + i)
                for i in range(servers_count)]

    def __link_all_servers(self):
        for i in range(len(self.servers)):
            neighbor_servers = self.servers.copy()
            neighbor_servers.pop(i)
            self.servers[i].set_servers(neighbor_servers)

    

