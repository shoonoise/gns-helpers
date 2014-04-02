import urllib.request
import urllib.parse
import urllib.error
import contextlib
import functools
import time

from ulib import validators
import ulib.validators.common # pylint: disable=W0611

from raava import worker
from gns import env


##### Public constants #####
S_GOLEM = "golem"

O_URL_RO        = "url-ro"
O_URL_RW        = "url-rw"
O_RECACHE_RESPS = "recache-resps"


###
CONFIG_MAP = {
    S_GOLEM: {
        O_URL_RO:        ("http://example.com", str),
        O_URL_RW:        ("http://example.com", str),
        O_RECACHE_RESPS: (60, lambda arg: validators.common.valid_number(arg, 0)),
    },
}


##### Exceptions #####
class GolemApiError(Exception):
    def __init__(self, body, err):
        super(GolemApiError, self).__init__()
        self._body = body
        self._err = err

    def __str__(self):
        msg = []
        try:
            msg.append(self._err.geturl())
        except Exception as err:
            msg.append(str(err))
        msg.append(str(self._err))
        msg.append(repr(self._body))
        return " ".join(msg)


##### Private methods #####
def _inner_get_responsibles(host):
    result = _golem_call("api/get_host_resp.sbml", { "host": host }).decode()
    return list(filter(None, result.strip().split(",")))

@functools.lru_cache(1)
def _cached_get_responsibles(host, every):
    return _inner_get_responsibles(host)

def _get_responsibles(host):
    every = env.get_config(S_GOLEM, O_RECACHE_RESPS)
    if every == 0: # No cache
        return _inner_get_responsibles(host)
    else:
        return _cached_get_responsibles(host, time.time() // every)

def _is_responsible(host, user):
    return ( user in _get_responsibles(host) )


###
def _golem_call(handle, attrs=None, data=None, ro=True):
    golem_url = env.get_config(S_GOLEM, ( O_URL_RO if ro else O_URL_RW ))
    golem_url += handle
    if attrs:
        golem_url += "?" + urllib.parse.urlencode(attrs)
    request = urllib.request.Request(golem_url, data=data)
    opener = urllib.request.build_opener()
    try:
        with contextlib.closing(opener.open(request)) as web_file:
            return web_file.read()
    except urllib.error.HTTPError as err:
        raise GolemApiError(err.read(), err)


##### On import #####
env.patch_config(CONFIG_MAP)


##### Provides #####
class golem: # pylint: disable=C0103
    get_responsibles = worker.make_task_method(_get_responsibles)
    is_responsible = worker.make_task_method(_is_responsible)

__all__ = (
    "golem",
)

