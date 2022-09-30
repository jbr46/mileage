import os
import requests
import urllib.parse
import random
import pymysql.cursors

from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def convert_code(code):
    connection = pymysql.connect(unix_socket='/cloudsql/mileage-364019:us-central1:mileage',
                            user='jbr46',
                            password='constituencies',
                            database='constituencies',
                            charset='utf8',
                            cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `station` FROM `stations` WHERE `code` = %s"
            cursor.execute(sql, (code,))
            station = cursor.fetchone()

    return station


def convert_station(station):
    connection = pymysql.connect(unix_socket='/cloudsql/mileage-364019:us-central1:mileage',
                            #host='34.171.138.243',
                            user='jbr46',
                            password='constituencies',
                            database='constituencies',
                            charset='utf8',
                            cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `code` FROM `stations` WHERE `station` = %s"
            cursor.execute(sql, (station,))
            code = cursor.fetchone()

    return code
