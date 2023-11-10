import pandas as pd

# Function to get product details from the user
def get_product_details(existing_prices):
    product_name = input("Enter product name: ")

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

csv_file_path = '/Users/easypoker/Documents/Digitalisering og applikationsudvikling/P7/frux/database.csv'

# Read existing prices from the CSV file
existing_prices_df = pd.read_csv(csv_file_path)
existing_prices = dict(zip(existing_prices_df['Product Name'], existing_prices_df['Price (DKK)']))

# Get user input for multiple products
products_data = []

while True:
    add_another = input("Do you want to add another product? (yes/no): ").lower()
    if add_another != 'yes':
        break

    product_details = get_product_details(existing_prices)
    if product_details['Price (DKK)'] is not None:
        products_data.append(product_details)

# Calculate the total price
total_price = sum(product['Price (DKK)'] for product in products_data)

# Display the total price
print(f"\nTotal Price for Selected Products: {total_price} DKK")
print("Products added successfully.")
