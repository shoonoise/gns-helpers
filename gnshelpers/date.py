import datetime
import dateutil.parser


##### Private classes #####
class date:  # pylint: disable=C0103
    workdays = tuple(range(0, 5))
    offdays = tuple(range(5, 7))

    def __init__(self, timestr):
        if timestr is not None:
            self.datetime = dateutil.parser.parse(timestr)
        else:
            self.datetime = datetime.datetime.now()

    @staticmethod
    def now():
        return date(None)

    @property
    def weekday(self):
        return self.datetime.weekday()  # pylint: disable=E1103

    @property
    def month(self):
        return self.datetime.month  # pylint: disable=E1103

for (name, value) in zip(
        ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec") +
        ("mon", "tue", "wed", "thu", "fri", "sat", "sun"),
        tuple(range(1, 13)) + tuple(range(7)),
    ):
    setattr(date, name, value)


##### Provides #####
__all__ = (
    "date",
)
