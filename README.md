# sales-analytics-system
Sales Analytics System – End-to-End Data Pipeline
Student Name: Amriza Farnaz
Student ID: bitsom_ba_2507592
Submission Date: 15/01/2026

📌 Project Overview

This project implements a complete sales analytics system that processes raw sales data, performs data cleaning and validation, executes analytical computations, integrates external product data via an API, enriches transactions, and generates a comprehensive text-based business report.

The system follows a modular ETL-style architecture and is designed to be robust, scalable, and exam-compliant, with proper error handling and user interaction.

🗂️ Repository Structure
sales-analytics-system/
  ├── README.md
  ├── main.py
  ├── utils/
  │   ├── file_handler.py
  │   ├── data_processor.py
  │   └── api_handler.py
  ├── data/
  │   └── sales_data.txt (provided)
  ├── output/
  └── requirements.txt


### 📦 Dependency Management

This project uses a `requirements.txt` file to manage external dependencies.
Currently, the only required third-party library is:

- requests

This ensures consistent setup across different systems.

### ⚙️ Technologies Used

- Python 3.x
- Standard Python libraries (`datetime`, `collections`, `os`)
- **requests** (third-party library for API integration)
- File-based processing (no external databases)

All external dependencies are listed in `requirements.txt`.


### 🔧 Setup & Run Instructions
## Step 1: Prerequisites

Ensure Python 3.x is installed on your system.

Check Python version:

python --version


or

python3 --version

## Step 2: Install Required Dependencies
All third-party dependencies are listed in `requirements.txt`.

Install them using:
```bash
python -m pip install -r requirements.txt
```
⚠️ Note: Dependency installation should be done via the command line, not inside Python files.


## Step 3: Project Folder Setup

Ensure the following folders exist in the project root:

data/
output/


If they do not exist, create them manually in VS Code:

Right-click → New Folder

Name them exactly: data and output

Step 4: Verify Input File

Ensure the raw sales data file exists in the project root:

sales_data.txt

Step 5: Run the Application

From the project root directory, run:

python main.py

Step 6: Output Files Generated

After successful execution, the following files will be created:

File	Description
data/enriched_sales_data.txt	API-enriched sales records
output/sales_report.txt	Final formatted analytics report
Step 7: Error Handling

Missing input files are handled gracefully

API failures do not crash the program

Invalid user inputs are safely handled

🧩 Functional Breakdown
🔹 Part 1: Data File Handling & Preprocessing

Reads sales data with encoding handling

Parses pipe-delimited records

Cleans numeric and text fields

Validates transactions using business rules

Produces clean, structured transaction dictionaries

🔹 Part 2: Data Processing & Analytics

Implements analytical functions including:

Total revenue calculation

Region-wise sales performance

Top selling products

Customer purchase analysis

Daily sales trends and peak sales day

Low-performing product detection

All analytics are implemented using lists, dictionaries, and functions.

🔹 Part 3: API Integration & Data Enrichment

Fetches product data from DummyJSON API

Creates fast product ID mappings

Enriches internal sales transactions with:

Product category

Brand

Rating

Match indicator

Saves enriched sales data to a new file

🔹 Part 4: Comprehensive Text Report

Generates a formatted report including:

Header & metadata

Overall sales summary

Region-wise performance

Top products and customers

Daily sales trends

Product performance analysis

API enrichment success summary

📄 Output: output/sales_report.txt

🔹 Part 5: Main Application

Provides a guided execution flow

Displays filter options and accepts user input

Executes all processing steps end-to-end

Handles errors gracefully

Prints clear progress updates to the console

### 🖥️ Sample Console Output
========================================
SALES ANALYTICS SYSTEM
========================================

[1/10] Reading sales data...
✓ Successfully read 95 transactions

[2/10] Parsing and cleaning data...
✓ Parsed 95 records

[3/10] Filter Options Available:
Regions: North, South, East, West
Amount Range: ₹500 - ₹90,000

Do you want to filter data? (y/n): n

[4/10] Validating transactions...
✓ Valid: 92 | Invalid: 3

[5/10] Analyzing sales data...
✓ Analysis complete

[6/10] Fetching product data from API...
✓ Fetched 30 products

[7/10] Enriching sales data...
✓ Enriched 85/92 transactions (92.4%)

[8/10] Saving enriched data...
✓ Saved to: data/enriched_sales_data.txt

[9/10] Generating report...
✓ Report saved to: output/sales_report.txt

[10/10] Process Complete!
========================================

### 🧠 Design Highlights

Modular architecture with clear separation of concerns

Pipeline-based data processing

Defensive programming with try–except blocks

Reusable analytics functions

Industry-style reporting output

✅ Conclusion

This project demonstrates a full data analytics lifecycle, from raw data ingestion to enriched reporting, combining core Python programming, data analysis, API integration, and software design best practices.
