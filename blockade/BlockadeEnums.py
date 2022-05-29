

class BlockadeAction:
    START = 'start'
    STOP = 'stop'
    RESTART = 'restart'
    KILL = 'kill'


class NetworkState:
    FAST = 'fast'
    SLOW = 'slow'
    DUPLICATE = 'duplicate'
    FLAKY = 'flaky'


class BlockadeVariables:
    IMAGE = "image"
    HOSTNAME = "hostname"
    PORTS = "ports"
    ENVIRONMENT = "environment"
