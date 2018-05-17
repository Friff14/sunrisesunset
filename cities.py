import sqlite3


def get_cities():
    conn = sqlite3.connect('cities.db')
    c = conn.cursor()

    cities = []
    for row in c.execute("SELECT name, state FROM city ORDER BY state, name"):
        cities.append({
            "city": row[0],
            "state": row[1]
        })

    return cities