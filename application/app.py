from flask import Flask, render_template, request, abort, redirect, session

# Library to read CSV datamase
import pandas as pd

# Library for secret key generation (for cache)
import os

# Initializing a Flask web application
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Global variable that holds a list of items the user has chosen
chosenItems = []

# Global variable for the database of grocery products
csv_url = 'https://raw.githubusercontent.com/Eberpraw/frux/5b6fcd790d597b263028317fce51a1db34af7dc5/database.csv'

# Flask syntax for creating our homepage and loading index.html
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profile/emilie", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        favorite_stores = request.form.getlist("store[]")
        session['favorite_stores'] = favorite_stores

    favorite_stores = session.get('favorite_stores', [])
    return render_template("profile/emilie.html", favorite_stores=favorite_stores)

# We create the grocery lists using GET & POST methods
@app.route("/grocery-list", methods=["GET", "POST"])
def grocery_list():
    # POST & GET method are used to get "name:"item" in input from index.html
    if request.method == "POST":
        item_input = request.form.get("item")
        # if no items are provided in form we abort
        if not item_input:
            return abort(400, "No item provided")

        # We create a list of strings where we strip spaces and separate items by a comma
        items = [item.strip() for item in item_input.split(',')]

        # Use a set to store unique items to prevent duplicates
        unique_items = set(items)

        # Add each item to chosenItems global variable
        chosenItems.extend(unique_items)

    # Get favorite stores from the session
    favorite_stores = session.get('favorite_stores', [])

    # split up items to a list (separated by comma) #list comp
    result = [item.strip() for sublist in chosenItems for item in sublist.split(',')]

    # Call the function to get prices based on chosen items
    supermarket_prices_by_store = get_product_details_by_store(chosenItems, favorite_stores)

    print("Supermarket Prices by Store:", supermarket_prices_by_store)

    # Render the template with the prices
    return render_template("grocery-list.html", supermarket_prices_by_store=supermarket_prices_by_store, chosenItems=result)


# Get the products from Rema 1000 in database.csv
def get_product_details(chosenItems_placeholder, favorite_stores):
    df = pd.read_csv(csv_url)

    # Convert 'Price (DKK)' column to numeric
    df['Price (DKK)'] = pd.to_numeric(df['Price (DKK)'])

    # Create a new variable with df variable, isin is a boolean that checks if chosenItem is in the database
    filtered_df = df[(df['Supermarket'].isin(favorite_stores)) & (df['Product Name'].isin(chosenItems_placeholder))]

    # We use zip to combine name and price into a dictionary
    product_price = dict(zip(filtered_df['Product Name'], filtered_df['Price (DKK)']))

    # Calculate the sum of prices
    total_price = sum(product_price.values())

    # Add total_price to the prices dictionary
    product_price['Total'] = total_price

    return product_price

# Function to get product details by store
def get_product_details_by_store(chosenItems_placeholder, favorite_stores):
    df = pd.read_csv(csv_url)

    # Convert 'Price (DKK)' column to numeric
    df['Price (DKK)'] = pd.to_numeric(df['Price (DKK)'])

    # Create a dictionary to hold prices for each store
    supermarket_prices_by_store = {store: {} for store in favorite_stores}

    # Iterate through the stores and chosen items to fill in the prices
    for store in favorite_stores:
        filtered_df = df[(df['Supermarket'] == store) & (df['Product Name'].isin(chosenItems_placeholder))]
        prices = dict(zip(filtered_df['Product Name'], filtered_df['Price (DKK)']))
        total_price = sum(prices.values())
        prices['Total'] = total_price
        supermarket_prices_by_store[store] = prices

    return supermarket_prices_by_store

