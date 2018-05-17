import requests as r
import textwrap

SPLIT_STRING = "h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m\n"
LEADING_CHARACTERS = 4
SUNSET_OFFSET = 5
CHARACTERS_PER_DAY = 11

class Year:
    block = []
    def __init__(self, url=None):
        if url:
            self.block = textwrap.wrap(r.get(url).text.split(SPLIT_STRING)[1][0:4185], 135)

    def get_value_by_date(self, month, day, rise=False):
        offset = (
                LEADING_CHARACTERS +
                (0 if rise else SUNSET_OFFSET) +
                CHARACTERS_PER_DAY * (month - 1)
        )
        return self.block[day - 1][offset:offset+5].strip()
