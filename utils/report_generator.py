"""
File: report_generator.py
Purpose: Generates sales reports from cleaned transaction data
"""
from datetime import datetime
from collections import defaultdict

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report
    """

    # -------------------------------
    # BASIC METRICS
    # -------------------------------

    total_transactions = len(transactions)
    total_revenue = sum(t["Quantity"] * t["UnitPrice"] for t in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted(t["Date"] for t in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    # -------------------------------
    # REGION-WISE PERFORMANCE
    # -------------------------------

    region_stats = defaultdict(lambda: {"sales": 0, "count": 0})

    for t in transactions:
        amount = t["Quantity"] * t["UnitPrice"]
        region_stats[t["Region"]]["sales"] += amount
        region_stats[t["Region"]]["count"] += 1

    region_summary = []
    for region, stats in region_stats.items():
        percentage = (stats["sales"] / total_revenue) * 100 if total_revenue else 0
        region_summary.append((region, stats["sales"], percentage, stats["count"]))

    region_summary.sort(key=lambda x: x[1], reverse=True)

    # -------------------------------
    # TOP 5 PRODUCTS
    # -------------------------------


    product_stats = defaultdict(lambda: {"qty": 0, "revenue": 0})

    for t in transactions:
        product_stats[t["ProductName"]]["qty"] += t["Quantity"]
        product_stats[t["ProductName"]]["revenue"] += t["Quantity"] * t["UnitPrice"]

    top_products = sorted(
        product_stats.items(),
        key=lambda x: x[1]["qty"],
        reverse=True
    )[:5]

    # -------------------------------
    # TOP 5 CUSTOMERS
    # -------------------------------

    customer_stats = defaultdict(lambda: {"spent": 0, "orders": 0})

    for t in transactions:
        customer_stats[t["CustomerID"]]["spent"] += t["Quantity"] * t["UnitPrice"]
        customer_stats[t["CustomerID"]]["orders"] += 1

    top_customers = sorted(
        customer_stats.items(),
        key=lambda x: x[1]["spent"],
        reverse=True
    )[:5]

    # -------------------------------
    # DAILY SALES TREND
    # -------------------------------

    daily_stats = defaultdict(lambda: {"revenue": 0, "count": 0, "customers": set()})

    for t in transactions:
        amount = t["Quantity"] * t["UnitPrice"]
        daily_stats[t["Date"]]["revenue"] += amount
        daily_stats[t["Date"]]["count"] += 1
        daily_stats[t["Date"]]["customers"].add(t["CustomerID"])

    daily_summary = sorted(
        [(d, v["revenue"], v["count"], len(v["customers"])) for d, v in daily_stats.items()]
    )

    # Best selling day
    best_day = max(daily_summary, key=lambda x: x[1])

    # -------------------------------
    # LOW PERFORMING PRODUCTS
    # -------------------------------

    low_products = [
        (p, v["qty"], v["revenue"])
        for p, v in product_stats.items()
        if v["qty"] < 10
    ]

    # -------------------------------
    # AVERAGE TRANSACTION VALUE PER REGION
    # -------------------------------
    avg_transaction_per_region = {}

# Loop through each region and calculate average transaction value
    for region, stats in region_stats.items():
        avg_transaction_per_region[region] = (
            stats["sales"] / stats["count"]
            if stats["count"] > 0 else 0
        )
    # -------------------------------
    # API ENRICHMENT SUMMARY
    # -------------------------------

    enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
    success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

    failed_products = {
        t["ProductName"]
        for t in enriched_transactions
        if not t.get("API_Match")
    }

    # -------------------------------
    # WRITE REPORT
    # -------------------------------

    with open(output_file, "w", encoding="utf-8") as f:

        # HEADER
        f.write("=" * 45 + "\n")
        f.write("          SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {total_transactions}\n")
        f.write("=" * 45 + "\n\n")

        # OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 45 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # REGION PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 45 + "\n")
        f.write("Region     Sales        % of Total   Transactions\n")
        for r, s, p, c in region_summary:
            f.write(f"{r:<10} ₹{s:>10,.0f}   {p:>6.2f}%        {c}\n")
        f.write("\n")

        # TOP PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 45 + "\n")
        f.write("Rank  Product        Qty   Revenue\n")
        for i, (p, v) in enumerate(top_products, 1):
            f.write(f"{i:<5} {p:<14} {v['qty']:<5} ₹{v['revenue']:,.0f}\n")
        f.write("\n")

        # TOP CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 45 + "\n")
        f.write("Rank  Customer   Total Spent   Orders\n")
        for i, (c, v) in enumerate(top_customers, 1):
            f.write(f"{i:<5} {c:<9} ₹{v['spent']:,.0f}     {v['orders']}\n")
        f.write("\n")

        # DAILY TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 45 + "\n")
        f.write("Date        Revenue     Transactions  Customers\n")
        for d, r, c, u in daily_summary:
            f.write(f"{d}  ₹{r:>8,.0f}     {c:<12} {u}\n")
        f.write("\n")

        # PRODUCT PERFORMANCE
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 45 + "\n")

        f.write(f"Best Selling Day: {best_day[0]} (₹{best_day[1]:,.0f})\n\n")

        f.write("Low Performing Products:\n")
        if low_products:
            for p, q, r in low_products:
                f.write(f" - {p}: Qty {q}, Revenue ₹{r:,.0f}\n")
        else:
            f.write(" - None\n")

        f.write("\n")

        f.write("Average Transaction Value per Region:\n")
        for region, avg in avg_transaction_per_region.items():
            f.write(f" - {region}: ₹{avg:,.2f}\n")

        f.write("\n")


        # API ENRICHMENT
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 45 + "\n")
        f.write(f"Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Not Enriched Products:\n")
        for p in failed_products:
            f.write(f" - {p}\n")

    print(f"Sales report generated successfully at: {output_file}")
