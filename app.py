import os
import datetime
import pymysql.cursors


from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from miles import initialise_graph, algorithm
from helpers import apology, login_required, convert_code, convert_station

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        start = request.form.get("origin")
        target = request.form.get("destination")
        g = initialise_graph()
        previous_nodes, shortest_path = algorithm(g, start)
        path = []
        node = target
        while node != start:
            path.append(node)
            node = previous_nodes[node]
        path.append(start)
        distance = round(shortest_path[target], 2)
        return render_template("result.html", distance=distance, path=" -> ".join(reversed(path)), origin=start, destination=target)
    else:
        return render_template("calculator.html")