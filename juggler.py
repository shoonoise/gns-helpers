import requests
import logging

from raava import worker


##### Private objects #####
_logger = logging.getLogger(__name__)


##### Public methods #####
def send_raw(to, host, service, status, description, instance=""):
    _logger.debug("Sending to Juggler: %s", to)
    ok = False
    try:
        result = requests.get("http://{}/juggler-fcgi.py".format(to), params={
                "host":        host,
                "service":     service,
                "instance":    instance,
                "status":      status,
                "description": description,
            })
        if result.status_code == 200 and result.text == "OK":
            _logger.info("Event sent to Juggler to %s, response: %s", to, result)
            ok = True
        else:
            _logger.error("Failed to send SMS to %s: %d %s; %s", to, result.status_code, result.reason, result.text)
    except Exception:
        _logger.exception("Failed to send SMS to %s", to)
    worker.get_current_task().checkpoint()
    return ok
