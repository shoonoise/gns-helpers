import smtplib
import email.mime.multipart
import email.mime.text
import email.utils
import email.header

import contextlib
import logging

from ulib import validators
import ulib.validators.common  # pylint: disable=W0611
import ulib.validators.network

from raava import worker
from gns import env

from . import common


##### Public constants #####
S_EMAIL  = "email"

O_SERVER   = "server"
O_SSL      = "ssl"
O_USER     = "user"
O_PASSWD   = "passwd"
O_FROM     = "from"
O_CC       = "cc"


###
CONFIG_MAP = {
    common.S_OUTPUT: {
        S_EMAIL: {
            O_SERVER: ("localhost",      lambda arg: validators.network.valid_ip_or_host(arg)[0]),
            O_SSL:    (False,            validators.common.valid_bool),
            O_USER:   (None,             validators.common.valid_empty),
            O_PASSWD: (None,             str),
            O_FROM:   ("root@localhost", str),
            O_CC:     ([],               validators.common.valid_string_list),
        },
    },
}


###
DEFAULT_SUBJECT_TEMPLATE = """
    Powny message: ${event.get("host", "<Host?>")}:${event.get("service", "<Service?>")}
"""

DEFAULT_BODY_TEMPLATE = """
    <%
        import yaml
        host = event.get("host", "<Host?>")
        service = event.get("service", "<Service?>")
        status = event.get("status", "<Status?>")
        dumper = lambda arg: yaml.dump(arg, default_flow_style=False, indent=4).strip()
        data = dumper(dict(event))
        extra = dumper(event.get_extra())
    %>
    The event ${host}:${service} is ${status}.

    Event:
    =====
    ${data}
    =====

    Extra information:
    =====
    ${extra}
    =====
"""


##### Private objects #####
_logger = logging.getLogger(__name__)


##### Public methods #####
def send_raw(to, subject, body, cc=(), extra_mime=None):
    to = validators.common.validStringList(to)
    cc = validators.common.validStringList(cc) + env.get_config(common.S_OUTPUT, S_EMAIL, O_CC)

    send_from = env.get_config(common.S_OUTPUT, S_EMAIL, O_FROM)

    current_task = worker.get_current_task()
    mime_headers = {"Powny-Job-Id": current_task.get_job_id(),
                    "Powny-Task-Id": current_task.get_task_id()}
    mime_headers.update(extra_mime)

    message = email.mime.multipart.MIMEMultipart()
    message["From"] = send_from
    message["To"] = ", ".join(to)
    if len(cc) != 0:
        message["CC"] = ", ".join(cc)
    message["Date"] = email.utils.formatdate(localtime=True)
    message["Subject"] = subject
    message.attach(email.mime.text.MIMEText(body))
    for name in mime_headers:
        header = email.header.Header(header_name=name, s=mime_headers[name])
        message[name] = header

    server_host = env.get_config(common.S_OUTPUT, S_EMAIL, O_SERVER)
    user = env.get_config(common.S_OUTPUT, S_EMAIL, O_USER)

    _logger.debug("Sending email to: %s; cc: %s; via SMTP %s@%s", to, cc, user, server_host)

    ok = False
    if not env.get_config(common.S_OUTPUT, common.O_NOOP):
        smtp_class = ( smtplib.SMTP_SSL if env.get_config(common.S_OUTPUT, S_EMAIL, O_SSL) else smtplib.SMTP )
        try:
            with contextlib.closing(smtp_class(server_host)) as client:
                if user is not None:
                    client.login(user, env.get_config(common.S_OUTPUT, S_EMAIL, O_PASSWD))
                client.sendmail(send_from, to + cc, message.as_string())
                _logger.info("Email sent to: %s; cc: %s", to, cc)
                ok = True
        except Exception:
            _logger.exception("Failed to send email to: %s; cc: %s", to, cc)
    else:
        _logger.info("Email sent to: %s; cc: %s (noop)", to, cc)
        ok = True
    worker.get_current_task().checkpoint()
    return ok

def send_event(to, event, subject=DEFAULT_SUBJECT_TEMPLATE, body=DEFAULT_BODY_TEMPLATE, cc=()):
    extra_mime = {'Powny-Juggler-Status': event.get("status"),
                  'Powny-Juggler-Host': event.get("host"),
                  'Powny-Juggler-Service': event.get("service")}
    return send_raw(to, env.format_event(subject, event), env.format_event(body, event), cc, extra_mime)
