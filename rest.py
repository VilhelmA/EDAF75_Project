from bottle import get, post, run, request, response, route
import sqlite3
import json
import string
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
    open(databaseFile, 'w').close()
    conn = sqlite3.connect(databaseFile)
    c = conn.cursor()
    data = ""
    with open('resetAndInit.txt', 'r') as myfile:
        data=myfile.read()
    print(data)
    c.executescript(data)

@get('/customers')
def pong():
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
    return format_response({"data": res})

@get('/ingredients')
def ingredients():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT  type, balance, unit
        FROM    inventory
        """
    )
    res = [{"type": type, "quantity": balance, "unit": unit}
        for (type, balance, unit) in c]
    response.status = 200
    return format_response({"data": res})

@get('/cookies')
def cookies():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT  name
        FROM    cookies
        ORDER   name DESC
        """
    )
    res = [{"name": name}
        for (name) in c]
    response.status = 200
    return format_response({"data": res})

@get('/recipes')
def recipes():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT  name, type, quantity, unit
        FROM    cookies
        JOIN    inventory
        USING   (X)
        ORDER   name DESC, type DESC
        """
    )
    res = [{"cookie": name, "ingredient": type, "quantity": balance, "unit": unit}
        for (name) in c]
    response.status = 200
    return format_response({"data": res})

@post('/pallets')
def pallets():
    queryDict = request.query
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON') #needed?

    # 15 cookies/bag, 10 bags/box,  36 boxes/pallet

    for row in c.execute(
        """
        SELECT  ingredient_name, amount*15*10*36 > balance AS inStock
        FROM    recipes
        JOIN    recipe_entries
        USING   (bar_code)
        JOIN    raw_materials
        USING   (ingredient_name)
        WHERE   name=?
        """, [queryDict.get('cookie')]
    ):

        print(row)

    try:
        # for row in c.execute(
        #     """
        #
        #     INSERT INTO pallets (performanceid, name, ticketid)
        #     VALUES 	(?, ?, ?)
        #     """, [queryDict.get('cookie')]
        # )
        return ("/pallets/%s"   % id)
    except sqlite3.IntegrityError:
        return ("Error")


run(host='localhost', port=8888, debug = True)
