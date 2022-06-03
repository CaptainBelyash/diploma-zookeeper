

class ZookeeperContainerData:
    def __init__(self, server_id, address, port, cluster_name='zoo', image='zookeeper'):
        self.server_id = server_id
        self.address = address
        self.port = port
        self.container_name = f'{cluster_name}{self.server_id}'
        self.image = image
        self.servers = []

    def set_container_id(self, container_id):
        self.container_id = container_id

    def add_server(self, server):
        self.servers.append(server)
        return self

    def set_servers(self, servers):
        self.servers = servers

    def get_server_variable(self):
        return f'server.{self.server_id}={self.address}:2888:3888;{self.port}'

    def get_cluster_servers_variable(self):
        result = ' '.join(container.get_server_variable() for container in self.servers)
        result += f' server.{self.server_id}=0.0.0.0:2888:3888;{self.port}'
        return result
