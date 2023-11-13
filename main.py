import pandas as pd
# from flask import Flask

# Function to get product details from the user
def get_product_details(existing_prices, product_name):
    # Check if the product already has a price in the CSV file
    if product_name in existing_prices:
        price_dkk = existing_prices[product_name]
        print(f"Existing price for {product_name}: {price_dkk} DKK")
    else:
        print(f"Price for {product_name} not found in the CSV file.")
        price_dkk = None

    return {
        'Product Name': product_name,
        'Price (DKK)': price_dkk,
    }

# Replace 'ee786ff7897e4963ea57b1dc0f2bd73724bf9190' with the actual commit hash or branch name
github_csv_url = 'https://raw.githubusercontent.com/Eberpraw/frux/ee786ff7897e4963ea57b1dc0f2bd73724bf9190/database.csv'

# Read existing prices from the CSV file
existing_prices_df = pd.read_csv(github_csv_url)
existing_prices = dict(zip(existing_prices_df['Product Name'], existing_prices_df['Price (DKK)']))

# Get user input for multiple products (comma-separated)
products_input = input("Enter product names (comma-separated): ")
selected_product_names = [name.strip() for name in products_input.split(',')]

# Get product details for each selected product
products_data = []
for product_name in selected_product_names:
    product_details = get_product_details(existing_prices, product_name)
    if product_details['Price (DKK)'] is not None:
        products_data.append(product_details)

# Calculate the total price
total_price = sum(product['Price (DKK)'] for product in products_data)

# Display the total price
print(f"\nTotal Price for Selected Products: {total_price} DKK")
print("Products added successfully.")
