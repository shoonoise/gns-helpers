import logging

from ulib import typetools

from raava import zoo
from raava import rules

from . import const
from . import storage


##### Private objects #####
_logger = logging.getLogger(__name__)


##### Private methods #####
def _add_previous(*fields):
    fields = sorted( fields or (
            const.EVENT.HOST,
            const.EVENT.SERVICE,
        ))
    def make_method(method):
        def wrap(event_root, **kwargs):
            check_id = typetools.object_hash([ event_root.get(field) for field in fields ])
            check_path = zoo.join("_state", check_id)
            version = event_root.get_extra()[rules.EXTRA.COUNTER]
            (kwargs["previous"], old_version, write_ok) = storage.replace(
                path=check_path,
                value=event_root,
                default=None,
                version=version,
                fatal_write=False,
            )
            if not write_ok:
                _logger.debug("Can't save event value (by fields %s) with version %d because the storage contains a newer version (%d)",
                    { key: event_root[key] for key in fields }, version, old_version)
            return method(event_root, **kwargs)
        return wrap
    return make_method

def _is_changed(previous, current, from_, to, field=None):
    if previous is None:
        return True
    if field is None:
        field = EVENT.STATUS
    is_changed = (
        (from_ is None or from_ == previous.get(field)) and
        (to is None or to == current.get(field)) and
        previous[field] != current[field]
    )
    return is_changed


##### Private classes #####
class state:
    add_previous = _add_previous
    is_changed = _is_changed


##### Provides #####
__all__ = (
    "state",
)

