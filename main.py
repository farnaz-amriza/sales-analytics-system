"""
Main Application Script
Sales Analytics System
"""

from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

from utils.report_generator import generate_sales_report


def main():
    """
    Main execution function
    """

    try:
        # ------------------------------------------------
        # HEADER
        # ------------------------------------------------
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # ------------------------------------------------
        # [1/10] READ SALES DATA
        # ------------------------------------------------
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # ------------------------------------------------
        # [2/10] PARSE & CLEAN
        # ------------------------------------------------
        print("\n[2/10] Parsing and cleaning data...")
        parsed_transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_transactions)} records")

        # ------------------------------------------------
        # [3/10] FILTER OPTIONS
        # ------------------------------------------------
        regions = sorted({t["Region"] for t in parsed_transactions})
        amounts = [t["Quantity"] * t["UnitPrice"] for t in parsed_transactions]

        print("\n[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        apply_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()

        if apply_filter == "y":
            selected_region = input("Enter region to filter: ").strip()
            min_amt = float(input("Enter minimum transaction amount: "))
            max_amt = float(input("Enter maximum transaction amount: "))

            parsed_transactions = [
                t for t in parsed_transactions
                if t["Region"] == selected_region
                and min_amt <= (t["Quantity"] * t["UnitPrice"]) <= max_amt
            ]

            print(f"✓ Records after filtering: {len(parsed_transactions)}")

        # ------------------------------------------------
        # [4/10] VALIDATION
        # ------------------------------------------------
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(parsed_transactions)
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # ------------------------------------------------
        # [5/10] DATA ANALYSIS (PART 2)
        # ------------------------------------------------
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_transactions)
        region_wise_sales(valid_transactions)
        top_selling_products(valid_transactions)
        customer_analysis(valid_transactions)
        daily_sales_trend(valid_transactions)
        find_peak_sales_day(valid_transactions)
        low_performing_products(valid_transactions)
        print("✓ Analysis complete")

        # ------------------------------------------------
        # [6/10] API FETCH
        # ------------------------------------------------
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products")

        # ------------------------------------------------
        # [7/10] ENRICH SALES DATA
        # ------------------------------------------------
        print("\n[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
        success_rate = (enriched_count / len(valid_transactions)) * 100
        print(f"✓ Enriched {enriched_count}/{len(valid_transactions)} transactions ({success_rate:.1f}%)")

        # ------------------------------------------------
        # [8/10] SAVE ENRICHED DATA
        # ------------------------------------------------
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print("✓ Saved to: data/enriched_sales_data.txt")

        # ------------------------------------------------
        # [9/10] GENERATE REPORT
        # ------------------------------------------------
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # ------------------------------------------------
        # [10/10] COMPLETE
        # ------------------------------------------------
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except FileNotFoundError:
        print("❌ ERROR: Sales data file not found. Please check file path.")

    except ValueError as ve:
        print("❌ ERROR: Invalid input provided.")
        print("Details:", ve)

    except Exception as e:
        print("❌ Unexpected error occurred.")
        print("Details:", e)


# ------------------------------------------------
# ENTRY POINT
# ------------------------------------------------
if __name__ == "__main__":
    main()
