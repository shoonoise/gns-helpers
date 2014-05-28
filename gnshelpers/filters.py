from raava import comparators
from raava.rules import match_event
from raava.rules import match_extra
from raava.rules import disable_handler


##### Private classes #####
class cmp:  # pylint: disable=C0103
    pass
for (name, comparator) in comparators.COMPARATORS_MAP.items():
    setattr(cmp, name, comparator)


##### Provides #####
__all__ = (
    "cmp",
    "match_event",
    "match_extra",
    "disable_handler",
)
