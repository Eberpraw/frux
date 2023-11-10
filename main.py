import pandas as pd

# Function to get product details from the user
def get_product_details(existing_prices):
    product_name = input("Enter product name: ")

    # Check if the product already has a price in the CSV file
    if product_name in existing_prices:
        price_dkk = existing_prices[product_name]
        print(f"Existing price for {product_name}: {price_dkk} DKK")
    else:
        print("INVALID PRODUCT")

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
    products_data.append(product_details)

# Convert the list of dictionaries to a DataFrame
products_df = pd.DataFrame(products_data)

# Append the DataFrame to the CSV file
products_df.to_csv(csv_file_path, mode='a', header=not pd.DataFrame(pd.read_csv(csv_file_path)).shape[0], index=False)

print("Products added successfully.")
