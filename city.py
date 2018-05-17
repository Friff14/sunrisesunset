import sys

from year import Year
import pandas as pd
from cities import get_cities
import csv

DEFAULT_START_YEAR = 2004
DEFAULT_END_YEAR = 2019
BASE_NAVY_URL = "http://aa.usno.navy.mil/cgi-bin/aa_rstablew.pl?ID=AA&year={year}&task=0&state={state}&place={city}"


class City:
    city = None
    state = None
    years = {}

    def __init__(self, city, state):
        self.city = city
        self.state = state

    def _generate_navy_url(self, year):
        return BASE_NAVY_URL.format(state=self.state, city=self.city, year=str(year))

    def _init_year(self, year):
        self.years[str(year)] = Year(self._generate_navy_url(year))

    def init_years(self, start=DEFAULT_START_YEAR, end=DEFAULT_END_YEAR):
        for year in range(start, end):
            self._init_year(year)

    def get_value_by_date(self, year, month, day, rise=False):
        if str(year) not in self.years:
            self._init_year(year)
        return self.years[str(year)].get_value_by_date(month, day, rise)


if __name__ == '__main__':
    cities = get_cities()

    rows = []

    if len(sys.argv) > 1:
        count = int(sys.argv[1])
        cities = cities[0:count]

    for iteration in cities:
        city = City(iteration['city'], iteration['state'])
        print("Initializing years for", city.city, ',', city.state)
        try:
            city.init_years(start=2004, end=2019)
        except Year.NavyDoesntHaveThatDataException:
            print("The Navy doesn't have that data. Skipping for now.")
            continue
        except Exception:
            print("There was a different error I hadn't anticipated.")
            continue
        print("Years initialized")

        for year in range(2004, 2019):
            datelist = pd.date_range(
                pd.datetime(day=1, month=1, year=year),
                pd.datetime(day=31, month=12, year=year)
            )
            row = [city.city, city.state, year]
            for date in datelist:
                if date.month == 3 and date.day == 1 and year % 4 != 0:
                    row.append('')
                    row.append('')
                row.append(city.get_value_by_date(date.year, date.month, date.day, rise=True))
                row.append(city.get_value_by_date(date.year, date.month, date.day, rise=False))

            rows.append(row)

        print("Data retrieved")

    first_row = ['City', 'State', 'Year']
    for x in range(0, 366):
        first_row.append('Rise ' + str(x + 1))
        first_row.append('Set ' + str(x + 1))

    with open("output.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(first_row)

        for row in rows:
            writer.writerow(row)
