import functools

from ulib import typetools
from ulib import validators
import ulib.validators.common  # pylint: disable=W0611

from gns import env

from . import via_email as email
from . import via_ya_sms as sms


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
        email.CONFIG_MAP,
        #sms.CONFIG_MAP,  # XXX: No config
    ))


##### On import #####
env.patch_config(CONFIG_MAP)


##### Provides #####
__all__ = (
    "email",
    "sms",
)
