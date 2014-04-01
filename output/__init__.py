import functools

from ulib import typetools
from ulib import validators
import ulib.validators.common # pylint: disable=W0611

from gns import env

from . import via_email
from . import via_ya_sms


##### Public constants #####
S_OUTPUT = "output"
O_NOOP = "noop"


###
CONFIG_MAP = functools.reduce(typetools.merge_dicts, (
        {
            S_OUTPUT: {
                O_NOOP: (False, validators.common.valid_bool),
            }
        },
        via_email.CONFIG_MAP,
        via_ya_sms.CONFIG_MAP,
    ))


##### On import #####
env.patch_config(CONFIG_MAP)


##### Provides #####
email = via_email.Email # pylint: disable=C0103
sms = via_ya_sms.Sms # pylint: disable=C0103

__all__ = (
    "email",
    "sms",
)

