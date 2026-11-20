# SmartCart AI

A college minor-project prototype for multi-category e-commerce comparison and predictive analytics.

## Features
- Multi-category product search and filters
- Demo listings representing Amazon, Flipkart, Myntra and Meesho
- Discount and lowest listed price comparison
- Ratings and review counts
- Basic TextBlob review sentiment analysis
- Scikit-learn Linear Regression price trend demonstration
- SQLite database and Chart.js comparison chart

## Setup (Windows / VS Code)

1. Install Python 3.11 or 3.12 and VS Code.
2. Open this folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:

   `python -m venv .venv`

5. Activate it in PowerShell:

   `.venv\\Scripts\\Activate.ps1`

   If PowerShell blocks activation, use Command Prompt terminal and run:

   `.venv\\Scripts\\activate.bat`
   6. Install packages:

   `python -m pip install -r requirements.txt`

7. Run:

   `python app.py`

8. Open http://127.0.0.1:5000 in your browser.

The SQLite database is created automatically on first run.

## Important academic note
Marketplace listings are sample data and are not live or verified offers. Real-time integrations require authorized APIs, affiliate feeds, or licensed data access. The price prediction uses synthetic example data and must not be represented as a reliable commercial forecast.


## Included product categories
Electronics, Clothing & Fashion, Skincare & Personal Care, Daily-Use Essentials, Home & Kitchen, Books & Stationery, Baby & Kids, and Sports & Fitness. Grocery & Food is excluded. All marketplace prices in the starter catalog are illustrative demo data.