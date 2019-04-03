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
    c.executescript(sqlScript)

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
        #   needed?
        #   c.execute('PRAGMA foreign_keys=ON')
        try:
            for row in c.execute(
                """
                INSERT INTO tickets (performanceid, name, ticketid)
                VALUES 	(?, ?, ?)
                """, [queryDict.get('user'), queryDict.get('pwd'), queryDict.get('performanceid')]
            ):
            return("/tickets/%s" % id)
        except sqlite3.IntegrityError:
            return ("Error")


run(host='localhost', port=8888, debug = True)
