from flask import Flask, render_template, request, abort, session

# Library to read CSV database
import pandas as pd

# Library for secret key generation (for cache)
import os

# Initializing a Flask web application
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.jinja_env.globals.update(enumerate=enumerate)

# Global variable that holds a list of items the user has chosen
chosenItems = []

# Global variable for the database of grocery products
csv_url = 'https://raw.githubusercontent.com/Eberpraw/frux/5b6fcd790d597b263028317fce51a1db34af7dc5/database.csv'

# Flask syntax for creating our homepage and loading index.html
@app.route("/")
def index(): 
    return render_template("index.html")

#We create the subpage How it works
@app.route("/how-it-works")
def How_it_works():
    return render_template("how-it-works.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def Contact():
    return render_template ("contact.html")

@app.route("/profile/emilie", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        favorite_stores = request.form.getlist("store[]")
        session['favorite_stores'] = favorite_stores

    favorite_stores = session.get('favorite_stores', [])

    # Retrieve and display all different iterations of items from the session
    items_list_history = session.get('items_list', [])

    return render_template("profile/emilie.html", favorite_stores=favorite_stores, items_list_history=items_list_history)

# We create the grocery lists using GET & POST methods
@app.route("/grocery-list", methods=["GET", "POST"])
def grocery_list():
    # POST & GET method are used to get "name:"item" in input from index.html
    if request.method == "POST":
        item_input = request.form.get("item")
        # if no items are provided in form we abort
        if not item_input:
            return abort(400, "No items provided")

        # We take the string and separate items by comma and remove spaces
        items = []
        for item in item_input.split(','):
            items.append(item.strip())


        # Use a set to store unique items to prevent duplicates
        unique_items = set(items)

        # Add each item to chosenItems global variable
        chosenItems.extend(unique_items)

        # Save the current items list to the session
        current_items_list = session.get('items_list', [])
        current_items_list.append(list(unique_items))
        session['items_list'] = current_items_list

    # Get favorite stores from session
    favorite_stores = session.get('favorite_stores', [])

    # Call the function to get prices based on chosen items
    supermarket_prices_by_store = get_product_details_by_store(chosenItems, favorite_stores)

    # Call the function that sorts stores by prices
    sorted_stores = bubble_sort_stores(supermarket_prices_by_store)

    #Clears variable for next search
    reset_chosenItems(chosenItems)

    # Render the template with the prices
    return render_template("grocery-list.html", supermarket_prices_by_store=supermarket_prices_by_store, sorted_stores=sorted_stores, store_logos=store_logos, chosenItems=chosenItems)

# Function to get product details by store
def get_product_details_by_store(chosenItems, favorite_stores):
    df = pd.read_csv(csv_url)

    # Convert 'Price (DKK)' column to numeric
    df['Price (DKK)'] = pd.to_numeric(df['Price (DKK)'])

    # Create a dictionary to hold prices for each store
    supermarket_prices_by_store = {store: {} for store in favorite_stores}

    # Iterate through the stores and chosen items to fill in the prices, and convert the product names to lowercase for case-insensitive
    for store in favorite_stores:
        chosen_items_lower = [item.lower() for item in chosenItems]
        filtered_df = df[(df['Supermarket'] == store) & (df['Product Name'].str.lower().isin(chosen_items_lower))]
        prices = dict(zip(filtered_df['Product Name'], filtered_df['Price (DKK)']))
        total_price = sum(prices.values())
        prices['Total'] = total_price
        supermarket_prices_by_store[store] = prices

    return supermarket_prices_by_store

def bubble_sort_stores(prices_by_store):
    # Making a list of the searched stores
    stores = list(prices_by_store)
    n = len(stores)

    # Performing a Bubble sort
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if prices_by_store[stores[j]]['Total'] > prices_by_store[stores[j + 1]]['Total']:
                stores[j], stores[j + 1] = stores[j + 1], stores[j]

    return stores    

store_logos = {
    'Rema 1000': '/static/images/Rema_logo.png',
    'Netto': '/static/images/Netto_logo.png',
    'Føtex': '/static/images/Føtex_logo.png',
    'Coop 365': '/static/images/Coop_logo.png',
    'Lidl': '/static/images/Lidl_logo.png',
}

# Function that clears variable
def reset_chosenItems(chosenItems):
    chosenItems.clear() 