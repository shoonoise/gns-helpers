import urllib.request
import urllib.parse
import urllib.error
import contextlib
import logging


##### Private objects #####
_logger = logging.getLogger(__name__)


##### Private methods #####
def send_raw(to, host, service, status, body, instance=""):
    request = urllib.request.Request(
        "http://{to}/juggler-fcgi.py?{query}".format(to=to, query=urllib.parse.urlencode({
                "host":        host,
                "service":     service,
                "instance":    instance,
                "status":      status,
                "description": body,
            }),
        ))
    opener = urllib.request.build_opener()
    _logger.debug("Sending to Juggler: %s", to)
    ok = False
    try:
        with contextlib.closing(opener.open(request)) as web_file:
            result = web_file.read().decode().strip()
        if result == "OK":
            _logger.info("Event sent to Juggler to %s, response: %s", to, result)
            ok = True
        else:
            _logger.error("Invalid response from Juggler-frontend (%s): %s", to, result)
    except urllib.error.HTTPError as err:
        result = err.read().decode().strip()
        _logger.exception("Failed to send SMS to %s, response: %s", to, result)
    except Exception:
        _logger.exception("Failed to send SMS to %s", to)
    return ok
