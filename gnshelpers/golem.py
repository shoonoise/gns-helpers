import functools
import time

import golemapi

from ulib import validators
import ulib.validators.common  # pylint: disable=W0611

from gns import env


##### Public constants #####
S_GOLEM = "golem"

O_URL_RO        = "url-ro"
O_URL_RW        = "url-rw"
O_CACHE_SIZE    = "cache-size"
O_RECACHE_EVERY = "recache-every"


###
CONFIG_MAP = {
    S_GOLEM: {
        O_URL_RO:        ("http://example.com", str),
        O_URL_RW:        ("http://example.com", str),
        O_CACHE_SIZE:    (10000, lambda arg: validators.common.valid_number(arg, 0)),
        O_RECACHE_EVERY: (60, lambda arg: validators.common.valid_number(arg, 1)),
    },
}
env.patch_config(CONFIG_MAP)


##### Public methods #####
def is_downtimed(host, service=None):
    every = env.get_config(S_GOLEM, O_RECACHE_EVERY)
    return _cached_is_downtimed(host, service, time.time() // every)

def get_responsibles(host):
    every = env.get_config(S_GOLEM, O_RECACHE_EVERY)
    return _cached_get_responsibles(host, time.time() // every)

def is_responsible(host, user):
    return ( user in get_responsibles(host) )

def send_sms_for_user(to, body):
    golem = golemapi.GolemApi(env.get_config(S_GOLEM, O_URL_RW))
    return golem.sms.send_for_user(to, body)


##### Private methods #####
@functools.lru_cache(env.get_config(S_GOLEM, O_CACHE_SIZE))
def _cached_is_downtimed(host, service, every):
    golem = golemapi.GolemApi(env.get_config(S_GOLEM, O_URL_RO))
    return ( golem.downtimes.get(host, service) is not None )

@functools.lru_cache(env.get_config(S_GOLEM, O_CACHE_SIZE))
def _cached_get_responsibles(host, every):
    golem = golemapi.GolemApi(env.get_config(S_GOLEM, O_URL_RO))
    return golem.hosts.get_responsibles(host)
