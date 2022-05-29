from blockade.BlockadeEnums import BlockadeVariables
from zookeeper import ZookeeperContainer


def get_zookeeper_blockade_container(server: ZookeeperContainer):
    return {
        BlockadeVariables.IMAGE: server.image,
        BlockadeVariables.HOSTNAME: server.container_name,
        BlockadeVariables.PORTS: [server.port],
        BlockadeVariables.ENVIRONMENT: {
            ZkEnvVar.ZOO_MY_ID: f"{server.server_id}",
            ZkEnvVar.ZOO_SERVERS: server.get_cluster_servers_variable(),
            ZkEnvVar.ZOO_4LW_COMMANDS_WHITELIST: "srvr, mntr, stat, ruok, conf, isro"
        }
    }


class ZkEnvVar:
    ZOO_MY_ID = "ZOO_MY_ID"
    ZOO_SERVERS = "ZOO_SERVERS"
    ZOO_4LW_COMMANDS_WHITELIST = "ZOO_4LW_COMMANDS_WHITELIST"
