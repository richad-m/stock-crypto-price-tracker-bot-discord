import requests
import os
# Use any db to stock informations about watchlist
from replit import db

WATCHLISTS = {"stocks": "watchlist",
              "crypto": 'crypto_watchlist'}

my_alpha_secret = os.environ['ALPHA']


def get_booba_quote():
    # Returns a random booba quote
    response = requests.get("https://api.booba.cloud")
    quote = response.json()["quote"]
    return ("\"{}\"").format(quote)


def get_growth(today_price, yesterday_price):
    # Returns relative growth between two int prices
    relative_growth = ((today_price-yesterday_price)/today_price) * 100
    round_growth = round(relative_growth, 2)
    if round_growth >= 0:
        return "+{}% :arrow_up:".format(round_growth)
    else:
        return "{}% :arrow_down:".format(round_growth)


def get_stock_price(tri):
    # Returns open price + growth on stock market using AlphaAvantage API
    response = requests.get(
        "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}".format(tri, my_alpha_secret))

    open_price = list(response.json()['Time Series (Daily)'].values())[
        0]['1. open']
    rounded_open_price = round(float(open_price), 2)

    previous_price = list(response.json()['Time Series (Daily)'].values())[
        3]['1. open']
    rounded_previous_price = round(float(previous_price), 2)

    growth = get_growth(rounded_open_price, rounded_previous_price)

    symbol = response.json()["Meta Data"]["2. Symbol"]
    return "{} stock opened at {}$ ({}) ".format(symbol, rounded_open_price, growth)


def add_stock_to_follow(stock, product):
    # Adds product to Watchlist
    watchlist = WATCHLISTS[product]
    if watchlist not in db.keys():
        # If no watchlist yet, create one
        db[watchlist] = []
        stocks = db[watchlist]
        stocks.append(stock)
        db[watchlist] = stocks
        response = "{} has beend added to followed stocks : {}".format(
            stock, ','.join(stocks))
    else:
        # If watchlist already exists
        if stock in db[watchlist]:
            # If asked stock already in watchlist, tell the user
            stocks = db[watchlist]
            response = "{} is already added to followed stocks : {}".format(
                stock, ", ".join(stocks))
        else:
            # If asked stock not in watchlist, add it and tell the new watchlist
            stocks = db[watchlist]
            stocks.append(stock)
            db[watchlist] = stocks
            response = "{} has beend added to followed stocks : {}".format(
                stock, ', '.join(stocks))
    return response


def stock_to_follow(product):
    # Display specified Watchlist to user
    watchlist = WATCHLISTS[product]
    if watchlist not in db.keys():
        # If there are no watchlist yet, tell the user
        response = "No stocks followed for now, add stocks with '!stocks AAPL for example'"
    else:
        # If there is a watchlist, display price for all products
        stocks = db[watchlist]
        response_list = []
        for stock in stocks:
            # Getting all prices and growth of the watchlist
            if product == 'stocks':
                # If stock watchlist, call get_stock_price
                response_list.append(get_stock_price(stock))
            elif product == 'crypto':
                # If crypto watchlist, call get_crypto_price
                response_list.append(get_crypto_price(stock))
        string_stocks = "\n- ".join(response_list)
        response = "Here are your followed {} :chart_with_upwards_trend: \n\n - {}".format(
            product, string_stocks)
    return response


def remove_stock_to_follow(stock, product):
    # Delete a product from a watchlist
    watchlist = WATCHLISTS[product]
    if watchlist not in db.keys():
        # If no watchlist exists, tell the user
        response = "No {} followed for now, add {} with '!stocks AAPL for example'".format(
            product, product)
    else:
        stocks = db[watchlist]
        string_stocks = ', '.join(stocks)
        try:
            # Try to delete stock from watchlist and confirm to the user
            stocks.remove(stock)
            db[watchlist] = stocks
            response = "{} has beend deleted to followed {} : {}".format(
                stock, product, string_stocks)
        except ValueError:
            # If stock not in current watchlist, tell the user
            response = "{} does not seem to be in your watchlist.Here is your current watchlist : {}".format(
                stock, string_stocks)
    return response


def get_crypto_price(crypto, fiat='EUR'):
    # Gets price and growth for a crypto by default in EUR, from alphavantage API
    response = requests.get(
        "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol={}&market={}&apikey={}".format(crypto, fiat, my_alpha_secret))

    open_price = list(response.json()['Time Series (Digital Currency Weekly)'].values())[
        0]['1a. open ({})'.format(fiat)]
    rounded_open_price = round(float(open_price), 2)

    previous_price = list(response.json()['Time Series (Digital Currency Weekly)'].values())[
        1]['1a. open ({})'.format(fiat)]
    rounded_previous_price = round(float(previous_price), 2)

    growth = get_growth(rounded_open_price, rounded_previous_price)

    symbol = response.json()["Meta Data"]["3. Digital Currency Name"]

    return "{} stock opened at {}{} ({}) ".format(symbol, rounded_open_price, fiat, growth)
