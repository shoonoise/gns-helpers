##### Public constants #####
class EVENT:
    HOST    = "host"
    SERVICE = "service"
    STATUS  = "status"
    DESC    = "description"


###
class STATUS:
    OK   = "OK" # pylint: disable=C0103
    INFO = "INFO"
    WARN = "WARN"
    CRIT = "CRIT"


##### Provides #####
__all__ = (
    "EVENT",
    "STATUS",
)

