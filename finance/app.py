import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    #db.execute("CREATE TABLE [IF NOT EXISTS] transactions (id INTEGER UNIQUE, user_id INTEGER, bought_or_sold TEXT, stock_symbol TEXT, price_per_share INTEGER, shares INTEGER, FOREIGN KEY(user_id) REFERENCES users(id);")

    symbol = request.form.get("symbol")
    if lookup(symbol) == None:
        return apology("Invalid stock name")

    shares = request.form.get("shares")
    try:
        shares = int(shares)
    except ValueError:
        return apology("Invalid number of shares")
    if shares < 1:
        return apology("Invalid number of shares")

    cash_available = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    purchase_price = lookup(symbol)["price"]
    price_total = purchase_price * shares
    if cash_available < price_total:
        return apology("Not enough funds to buy stock")

    db.execute("INSERT INTO transactions (user_id, bought_or_sold, stock_symbol, price_per_share, shares), VALUES(?, ?, ?, ?, ?)", session["user_id"], symbol, "bought", purchase_price, shares)


    return redirect("/history")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        symbol = request.form.get("symbol")
        if lookup(symbol) == None:
            return render_template("quote.html")
        dict = lookup(symbol)
        symbol = dict["symbol"]
        price = dict["price"]
        price = usd(price)
        return render_template("quoted.html", symbol=symbol, price=price)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    #checks for repeated usernames

    if not username or not password or not confirmation:
        return apology("One of the fields is empty")

    if confirmation != password:
        return apology("passwords do not match")
    has_repeat = False
    usernames = db.execute("SELECT username FROM users")
    for dict in usernames:
        for key in dict:
            if dict[key] == username:
                has_repeat = True
    if has_repeat:
        return apology("Username already exists, try another username")

    db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
    return render_template("login.html")
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
