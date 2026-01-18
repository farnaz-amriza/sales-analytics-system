## Task 2.1 : sales summary calculator ##

#a) Calculate Total Revenue
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns:
    float: total revenue (sum of Quantity * UnitPrice)
    """

    # Step 1: Initialize total revenue to 0
    total_revenue = 0.0

    # Step 2: Loop through each transaction dictionary
    for txn in transactions:

        # Step 3: Calculate revenue for one transaction
        # Revenue = Quantity * UnitPrice
        transaction_revenue = txn["Quantity"] * txn["UnitPrice"]

        # Step 4: Add transaction revenue to total revenue
        total_revenue += transaction_revenue

    # Step 5: Return final total revenue
    return total_revenue

#b) Calculate Revenue by Region
def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns:
    dictionary containing region-wise statistics
    """

    # Step 1: Dictionary to store region-wise aggregation
    region_stats = {}

    # Step 2: Calculate total sales across all regions
    total_sales = 0.0

    for txn in transactions:
        # Calculate transaction amount
        amount = txn["Quantity"] * txn["UnitPrice"]

        # Add to overall total sales
        total_sales += amount

        # Get region name
        region = txn["Region"]

        # Step 3: Initialize region entry if not present
        if region not in region_stats:
            region_stats[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        # Step 4: Update region totals
        region_stats[region]["total_sales"] += amount
        region_stats[region]["transaction_count"] += 1

    # Step 5: Calculate percentage contribution per region
    for region in region_stats:
        percentage = (region_stats[region]["total_sales"] / total_sales) * 100
        region_stats[region]["percentage"] = round(percentage, 2)

    # Step 6: Sort regions by total_sales in descending order
    sorted_region_stats = dict(
        sorted(
            region_stats.items(),
            key=lambda item: item[1]["total_sales"],
            reverse=True
        )
    )

    # Step 7: Return sorted dictionary
    return sorted_region_stats

#c) Calculate Top N Products by Revenue
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns:
    list of tuples in the format:
    (ProductName, TotalQuantity, TotalRevenue)
    """

    # Step 1: Dictionary to store aggregated product data
    product_stats = {}

    # Step 2: Loop through each transaction
    for txn in transactions:

        # Extract required fields
        product_name = txn["ProductName"]
        quantity = txn["Quantity"]
        unit_price = txn["UnitPrice"]

        # Calculate revenue for this transaction
        revenue = quantity * unit_price

        # Step 3: Initialize product entry if not already present
        if product_name not in product_stats:
            product_stats[product_name] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        # Step 4: Aggregate quantity and revenue
        product_stats[product_name]["total_quantity"] += quantity
        product_stats[product_name]["total_revenue"] += revenue

    # Step 5: Convert dictionary into list of tuples
    product_list = [
        (
            product,
            stats["total_quantity"],
            stats["total_revenue"]
        )
        for product, stats in product_stats.items()
    ]

    # Step 6: Sort products by total quantity sold (descending)
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Step 7: Return top n products
    return product_list[:n]

#d) Customer Purchase Analysis
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns:
    dictionary of customer statistics sorted by total_spent (descending)
    """

    #Dictionary to store customer-level aggregation
    customer_stats = {}

    #Loop through each transaction
    for txn in transactions:

        # Extract required fields
        customer_id = txn["CustomerID"]
        product_name = txn["ProductName"]
        quantity = txn["Quantity"]
        unit_price = txn["UnitPrice"]

        # Calculate transaction amount
        transaction_amount = quantity * unit_price

        #Initialize customer entry if not already present
        if customer_id not in customer_stats:
            customer_stats[customer_id] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()   # set ensures uniqueness
            }

        #Update total spent
        customer_stats[customer_id]["total_spent"] += transaction_amount

        # Increment purchase count
        customer_stats[customer_id]["purchase_count"] += 1

        # Add product to set (avoids duplicates)
        customer_stats[customer_id]["products_bought"].add(product_name)

    # Calculate average order value and convert set to list
    for customer_id in customer_stats:
        total_spent = customer_stats[customer_id]["total_spent"]
        purchase_count = customer_stats[customer_id]["purchase_count"]

        # Calculate average order value
        avg_order_value = total_spent / purchase_count

        # Store average order value
        customer_stats[customer_id]["avg_order_value"] = round(avg_order_value, 2)

        # Convert products set to list for final output
        customer_stats[customer_id]["products_bought"] = list(
            customer_stats[customer_id]["products_bought"]
        )

    # Sort customers by total_spent in descending order
    sorted_customer_stats = dict(
        sorted(
            customer_stats.items(),
            key=lambda item: item[1]["total_spent"],
            reverse=True
        )
    )

    # Return sorted customer statistics
    return sorted_customer_stats

## Task 2.2. Date-based analysis ##
# a) Daily Sales Trend
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns:
    dictionary sorted by date containing:
    - revenue
    - transaction_count
    - unique_customers
    """

    # Dictionary to store daily aggregates
    daily_summary = {}

    # Loop through each transaction
    for txn in transactions:

        # Extract required fields
        date = txn["Date"]
        customer_id = txn["CustomerID"]
        quantity = txn["Quantity"]
        unit_price = txn["UnitPrice"]

        # Calculate transaction revenue
        revenue = quantity * unit_price

        # Initialize date entry if not present
        if date not in daily_summary:
            daily_summary[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()  # set ensures uniqueness
            }

        # Update daily revenue
        daily_summary[date]["revenue"] += revenue

        # Increment transaction count
        daily_summary[date]["transaction_count"] += 1

        # Track unique customers
        daily_summary[date]["unique_customers"].add(customer_id)

    # Convert customer sets to counts
    for date in daily_summary:
        daily_summary[date]["unique_customers"] = len(
            daily_summary[date]["unique_customers"]
        )

    # Sort dictionary by date (chronologically)
    daily_summary_sorted = dict(sorted(daily_summary.items()))

    # Return sorted daily sales trend
    return daily_summary_sorted


# b) find Peak Sales Day
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns:
    tuple (date, revenue, transaction_count)
    """

    # Reuse daily sales trend
    daily_summary = daily_sales_trend(transactions)

    #Track peak values
    peak_date = None
    max_revenue = 0.0
    peak_transactions = 0

    # Loop through daily data
    for date, stats in daily_summary.items():

        # Compare revenues
        if stats["revenue"] > max_revenue:
            max_revenue = stats["revenue"]
            peak_date = date
            peak_transactions = stats["transaction_count"]

    # Return peak sales day details
    return (peak_date, round(max_revenue, 2), peak_transactions)

# Task 2.3: Low Performing Products
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales performance

    Returns:
    list of tuples:
    (ProductName, TotalQuantity, TotalRevenue)
    """

    # Dictionary to aggregate product data
    product_summary = {}

    # Loop through each transaction
    for txn in transactions:

        # Extract required fields
        product_name = txn["ProductName"]
        quantity = txn["Quantity"]
        unit_price = txn["UnitPrice"]

        # Calculate revenue for this transaction
        revenue = quantity * unit_price

        # Initialize product entry if not already present
        if product_name not in product_summary:
            product_summary[product_name] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        # Accumulate quantity
        product_summary[product_name]["total_quantity"] += quantity

        #Accumulate revenue
        product_summary[product_name]["total_revenue"] += revenue

    # Filter products with total quantity below threshold
    low_performance_list = []

    for product_name, stats in product_summary.items():
        if stats["total_quantity"] < threshold:
            low_performance_list.append(
                (
                    product_name,
                    stats["total_quantity"],
                    round(stats["total_revenue"], 2)
                )
            )

    # Sort by TotalQuantity in ascending order
    low_performance_list.sort(key=lambda x: x[1])

    # Return final list
    return low_performance_list
