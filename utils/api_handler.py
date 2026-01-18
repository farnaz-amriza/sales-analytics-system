## Task 3.1: Fetch Product Details ##
# a) Fetch Products from DummyJSON API
# install dependencies: requests (python -m pip install requests)
import requests  # Used to make HTTP requests to the API


def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns:
    list of product dictionaries

    If API call fails:
    - Returns empty list
    - Prints failure message
    """

    # Base URL for DummyJSON products API
    url = "https://dummyjson.com/products?limit=100"

    try:
        # Step 1: Send GET request to the API
        response = requests.get(url, timeout=10)

        # Step 2: Raise exception for HTTP error codes (4xx, 5xx)
        response.raise_for_status()

        # Step 3: Convert response to JSON
        data = response.json()

        # Step 4: Extract products list from response
        products = data.get("products", [])

        # Step 5: Prepare cleaned product list
        cleaned_products = []

        for product in products:
            cleaned_products.append({
                "id": product.get("id"),
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "price": product.get("price"),
                "rating": product.get("rating")
            })

        # Step 6: Print success message
        print(f"API SUCCESS: Fetched {len(cleaned_products)} products")

        # Step 7: Return cleaned product list
        return cleaned_products

    except requests.exceptions.RequestException as e:
        # Handles network errors, timeout errors, HTTP errors
        print("API FAILURE: Unable to fetch products")
        print("Error:", e)

        # Step 8: Return empty list on failure
        return []


# b) Create Product Mapping
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product information

    Parameters:
    - api_products: list of product dictionaries from fetch_all_products()

    Returns:
    - dictionary mapping product IDs to product info
    """

    # Step 1: Initialize empty dictionary for product mapping
    product_mapping = {}

    # Step 2: Loop through each product from API response
    for product in api_products:

        # Extract product ID
        product_id = product.get("id")

        # Skip product if ID is missing
        if product_id is None:
            continue

        # Step 3: Map product ID to required product attributes
        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    # Step 4: Return final product mapping
    return product_mapping

## Task 3.2: Enrich Transactions with Product Info ##
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches sales transactions with API product information

    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()

    Returns:
    - list of enriched transaction dictionaries
    """

    enriched_transactions = []

    # Loop through each transaction
    for txn in transactions:

        # Create a copy to avoid modifying original data
        enriched_txn = txn.copy()

        # Extract numeric part of ProductID (P101 -> 101)
        product_id_raw = txn.get("ProductID", "")
        api_product_id = None

        if product_id_raw.startswith("P"):
            try:
                api_product_id = int(product_id_raw[1:])
            except ValueError:
                api_product_id = None

        # Check if product exists in API mapping
        if api_product_id in product_mapping:
            api_info = product_mapping[api_product_id]

            enriched_txn["API_Category"] = api_info.get("category")
            enriched_txn["API_Brand"] = api_info.get("brand")
            enriched_txn["API_Rating"] = api_info.get("rating")
            enriched_txn["API_Match"] = True
        else:
            # Step 4: Handle non-matching products
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        # Append enriched transaction
        enriched_transactions.append(enriched_txn)

    return enriched_transactions

#Saving enriched data to a file
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions to a pipe-delimited text file

    Parameters:
    - enriched_transactions: list of enriched transaction dictionaries
    - filename: output file path
    """

    # Define header columns (original + API fields)
    headers = [
        "TransactionID",
        "Date",
        "ProductID",
        "ProductName",
        "Quantity",
        "UnitPrice",
        "CustomerID",
        "Region",
        "API_Category",
        "API_Brand",
        "API_Rating",
        "API_Match"
    ]

    # Open file for writing
    with open(filename, "w", encoding="utf-8") as file:

        # Write header row
        file.write("|".join(headers) + "\n")

        # Write each enriched transaction
        for txn in enriched_transactions:
            row = [
                str(txn.get(col, "")) if txn.get(col) is not None else ""
                for col in headers
            ]
            file.write("|".join(row) + "\n")

    print(f"Enriched data saved successfully to {filename}")
