from flask import Flask, render_template, request, abort, redirect
import pandas as pd

app = Flask(__name__)

chosenItems = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/items", methods=["GET", "POST"])
def items():
    if request.method == "POST":
        item_input = request.form.get("item")
        if not item_input:
            return abort(400, "No item provided")
        
        # Process the input items as needed
        items = [item.strip() for item in item_input.split(',')]
        
        # Add each item to chosenItems
        chosenItems.extend(items)
        
        return redirect("/grocery-list")
    else:
        return render_template("items.html")

@app.route("/grocery-list")
def grocery_list():
    # Call the function to get prices based on chosen items
    supermarket_prices = get_product_details_rema1000(chosenItems)

    # split up items to a list (separated by comma) 
    result = [item.strip() for sublist in chosenItems for item in sublist.split(',')]

    # Render the template with the prices
    return render_template("grocery-list.html", supermarket_prices=supermarket_prices, chosenItems=result)


# Get the products from Rema 1000 in database.csv
def get_product_details_rema1000(chosen_items, supermarket='Rema 1000', csv_url='https://raw.githubusercontent.com/Eberpraw/frux/5b6fcd790d597b263028317fce51a1db34af7dc5/database.csv'):
    df = pd.read_csv(csv_url)

    # Filter rows based on supermarket and chosen items
    filtered_df = df[(df['Supermarket'] == supermarket) & (df['Product Name'].isin(chosen_items))]

    # Create a dictionary of product names and prices
    prices = dict(zip(filtered_df['Product Name'], filtered_df['Price (DKK)']))

    print("Supermarket Prices:", prices)

    return prices