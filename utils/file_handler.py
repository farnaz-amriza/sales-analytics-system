"""
File: file_handler.py
Purpose: Handles file reading with encoding and error management
"""
## Task 1.1: Read sales data with encoding handling ##
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)

    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]
    """
    # Handle encoding issues
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

                # Skip header row
                lines = lines[1:]

                # Remove empty lines and strip newline characters
                cleaned_lines = [line.strip() for line in lines if line.strip()]

                return cleaned_lines

        except UnicodeDecodeError:
            # Try next encoding
            continue

        except FileNotFoundError:
            print(f"Error: File not found -> {filename}")
            return []

    # If no encoding worked, print error message
    print("Error: Unable to read file due to encoding issues.")
    return []

## Task 1.2: Parse and Clean Data ##
def parse_transactions(raw_lines):
    """
    Parses raw transaction lines into a clean list of dictionaries
    """

    # List to store cleaned transaction dictionaries
    parsed_transactions = []

    # Loop through each raw transaction line
    for line in raw_lines:

        # Split the line using pipe delimiter
        fields = line.split("|")

        # Skip rows that do not have exactly 8 fields
        if len(fields) != 8:
            continue

        # Unpack fields into variables
        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = fields

        # Clean ProductName
        # Remove commas (e.g., Mouse,Wireless → Mouse Wireless)
        product_name = product_name.replace(",", " ")

        # Clean and convert Quantity
        # Remove commas and convert to int
       
        quantity = quantity.replace(",", "")
        quantity = int(quantity)

       # Clean and convert UnitPrice
        # Remove commas and convert to float
        unit_price = unit_price.replace(",", "")
        unit_price = float(unit_price)

        # Create cleaned transaction dictionary
        transaction = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        # Add cleaned transaction to the result list
        parsed_transactions.append(transaction)

    # Return list of cleaned transaction dictionaries
    return parsed_transactions

## Task 1.3: Data Validation and Filtering ##

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Returns:
    (valid_transactions, invalid_count, filter_summary)
    """

    valid_transactions = []
    invalid_count = 0

    # Counters for summary
    filtered_by_region = 0
    filtered_by_amount = 0

    total_input = len(transactions)

    
    # Validation Phase
  
    for txn in transactions:

        # Check required fields exist
        required_fields = [
            "TransactionID", "ProductID", "CustomerID",
            "Quantity", "UnitPrice", "Region"
        ]

        if not all(field in txn and txn[field] for field in required_fields):
            invalid_count += 1
            continue

        # Validation rules
        if txn["Quantity"] <= 0:
            invalid_count += 1
            continue

        if txn["UnitPrice"] <= 0:
            invalid_count += 1
            continue

        if not txn["TransactionID"].startswith("T"):
            invalid_count += 1
            continue

        if not txn["ProductID"].startswith("P"):
            invalid_count += 1
            continue

        if not txn["CustomerID"].startswith("C"):
            invalid_count += 1
            continue

        # If all validations pass, keep the transaction
        valid_transactions.append(txn)

   
    # Filtering Phase
  
    filtered_transactions = []

    for txn in valid_transactions:
        transaction_amount = txn["Quantity"] * txn["UnitPrice"]

        # Apply region filter
        if region and txn["Region"] != region:
            filtered_by_region += 1
            continue

        # Apply amount filters
        if min_amount and transaction_amount < min_amount:
            filtered_by_amount += 1
            continue

        if max_amount and transaction_amount > max_amount:
            filtered_by_amount += 1
            continue

        filtered_transactions.append(txn)

   
    # Filter Summary
   
    filter_summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered_transactions)
    }


    # Display filter info
   
    print("Available regions:", sorted(set(t["Region"] for t in transactions)))
    print(f"Transaction amount filter: min={min_amount}, max={max_amount}")
    print(f"Records after filtering: {len(filtered_transactions)}")

    return filtered_transactions, invalid_count, filter_summary
 