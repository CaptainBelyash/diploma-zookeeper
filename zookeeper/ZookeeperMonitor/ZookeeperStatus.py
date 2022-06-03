
class ZookeeperStatus:
    def __init__(self, mode=None, unavailable_time=None, election_time=None):
        self.is_ok = mode is not None
        self.mode = mode

        self.unavailable_time = unavailable_time
        self.election_time = election_time


class NodeMode:
    LEADER = 'leader'
    FOLLOWER = 'follower'


class Metric:
    def __init__(self, avg_t, min_t, max_t, count, sum_t):
        self.avg = avg_t
        self.min = min_t
        self.max = max_t
        self.cnt = count
        self.sum = sum_t
