import logging

from ulib import validators
import ulib.validators.common # pylint: disable=W0611

from raava import worker
from gns import env

from . import common
from .. import golem


##### Public constants #####
DEFAULT_BODY_TEMPLATE = """
    <%
        import time
        now = time.strftime("%H:%M.%S %d-%m-%Y")
        host = event.get("host", "<Host?>")
        service = event.get("service", "<Service?>")
        status = event.get("status", "<Status?>")
    %>
    ${now} ${host}:${service} = ${status}
"""


##### Private objects #####
_logger = logging.getLogger(__name__)


##### Private methods #####
def _send_raw(task, to, body):
    to = validators.common.valid_string_list(to)
    _logger.debug("Sending to Golem SMS API: %s", to)
    ok = False
    if not env.get_config(common.S_OUTPUT, common.O_NOOP):
        try:
            golem.send_sms_for_user(to, body)
            ok = True
        except Exception:
            _logger.exception("Failed to send SMS to %s", to)
    else:
        _logger.info("SMS sent to Golem (noop) to %s", to)
        ok = True
    task.checkpoint()
    return ok

def _send_event(task, to, event, body=DEFAULT_BODY_TEMPLATE):
    return _send_raw(task, to, env.format_event(body, event))


##### Public methods #####
send_raw = worker.make_task_method(_send_raw) # pylint: disable=C0103
send_event = worker.make_task_method(_send_event) # pylint: disable=C0103
