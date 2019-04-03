from bottle import get, post, run, request, response, route
import sqlite3
import json
import string
import datetime
from random import *
databaseFile = "applications.sqlite"
resetCode="resetAndInit.txt"
conn = sqlite3.connect(databaseFile)

@get('/ping')
def pong():
    response.content_type = 'text'
    return ("pong %r" % response.status)

@post('/reset')
def resetDatabase():
    print('RESET!')
    #open(databaseFile, 'w').close()
    #conn = sqlite3.connect(databaseFile)
    c = conn.cursor()
    data = ""
    with open('resetAndInit.txt', 'r') as myfile:
        data=myfile.read()
    print(data)
    c.executescript(data)

@get('/customers')
def customers():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT  *
        FROM    customers
        """
    )
    res = [{"name": name, "address": address}
        for (name, address) in c]
    response.status = 200
    return format_response({"customers": res})

@get('/raw_materials')
def materials():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT  ingredient_name, balance
        FROM    raw_materials
        """
    )
    res = [{"name": ingredient_name, "balance": balance}
        for (ingredient_name, balance) in c]
    response.status = 200
    return format_response({"materials": res})

@get('/ingredients')
def ingredients():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT  ingredient_name, balance, unit
        FROM    raw_materials
        """
    )
    res = [{"name": type, "quantity": balance, "unit": unit}
        for (type, balance, unit) in c]
    response.status = 200
    return format_response({"ingredients": res})

@get('/cookies')
def cookies():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT name
        FROM recipes
        ORDER BY name DESC
        """
    )
    res = [{"name": name}
        for (name) in c]
    response.status = 200
    return format_response({"cookies": res})

@get('/recipes')
def recipes():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT  name, ingredient_name, amount, unit
        FROM    recipes
        JOIN    recipe_entries
        USING   (bar_code)
        JOIN    raw_materials
        USING   (ingredient_name)
        ORDER BY name ASC, ingredient_name ASC
        """
    )
    res = [{"cookie": name, "ingredient": ingredient_name, "quantity": amount, "unit": unit}
        for (name, ingredient_name, amount, unit) in c]
    response.status = 200
    return format_response({"recipes": res})

@post('/pallets')
def pallets():
    queryDict = request.query
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON') #needed?
    # 15 cookies/bag, 10 bags/box,  36 boxes/pallet
    # c.execute("
    #     """
    #     SELECT name
    #     FROM recipe
    #
    #     """)

    c.execute(
        """
        SELECT name, bar_code
        FROM recipes
        WHERE name=?
        """, [queryDict.get('cookie')]
        )

    result = c.fetchall()
    print(result)
    bar_code = result[0][1]
    date = datetime.date
    time = datetime.time

    if len(result) < 1:
        print("no such cookie")
        return format_response({"status": "no such cookie"})
    for row in c.execute(
        """
        SELECT  ingredient_name, amount*15*10*36/100 < balance AS inStock
        FROM    recipes
        JOIN    recipe_entries
        USING   (bar_code)
        JOIN    raw_materials
        USING   (ingredient_name)
        WHERE   name=?
        """, [queryDict.get('cookie')]
    ):
        if (row[1] != 1):
            return format_response({"status": "not enough ingredients"})
    try:
        print("before exec")
        c.execute(
        """
            INSERT INTO pallets (bar_code, pallet_time, pallet_date, is_blocked)
            VALUES 	(?, ?, ?, ?)

        """, [int(bar_code), str(datetime.datetime.now().time()), str(datetime.datetime.now().date()), 0]
        )
        print("after exec")
        return ("/pallets/%s"   % id)
    except sqlite3.IntegrityError as error:
        return (error)

@post('/block/<cookie_name>/<from_date>/<to_date>')
def block(cookie_name, from_date, to_date):
    print(cookie_name, from_date, to_date)
    c.execute(
    """
    WITH corresponding_code AS (
        SELECT  bar_code
        FROM    recipes
        WHERE   name= ?
    ),
    bad_pallets AS (
        SELECT  pallet_nbr
        FROM    pallets
        WHERE   pallet_date BETWEEN ? AND ?
                AND bar_code IN (SELECT bar_code FROM corresponding_code)
    )
    UPDATE  pallets
    SET     isBlocked = 1
    WHERE   pallet_nbr IN (SELECT pallet_nbr FROM bad_pallets)
    """, [cookie_name,from_date, to_date]
    )
    return format_response({"status": "ok"})

@post('/unblock/<cookie_name>/<from_date>/<to_date>')
def unblock(cookie_name, from_date, to_date):
    print(cookie_name, from_date, to_date)
    c.execute(
    """
    WITH corresponding_code AS (
        SELECT  bar_code
        FROM    recipes
        WHERE   name= ?
    ),
    bad_pallets AS (
        SELECT  pallet_nbr
        FROM    pallets
        WHERE   pallet_date BETWEEN ? AND ?
                AND bar_code IN (SELECT bar_code FROM corresponding_code)
    )
    UPDATE  pallets
    SET     isBlocked = 0
    WHERE   pallet_nbr IN (SELECT pallet_nbr FROM bad_pallets)
    """, [cookie_name,from_date, to_date]
    )
    return format_response({"status": "ok"})


def url(resource):
    return "http://{HOST}:{PORT}{resource}"

def format_response(d):
    return json.dumps(d, indent=4) + "\n"

run(host='localhost', port=8888, debug = True)
