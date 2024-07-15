responseMockData = {
    "Extracted Data": {
        "Company Name": "RetailCo",
        "Industry": "Retail",
        "Market Capitalization": 2000,
        "Revenue (in millions)": 800,
        "EBITDA (in millions)": 150,
        "Net Income (in millions)": 40,
        "Debt (in millions)": 110,
        "Equity (in millions)": 400,
        "Enterprise Value (in millions)": 2100,
        "P/E Ratio": 20,
        "Revenue Growth Rate (%)": 8,
        "EBITDA Margin (%)": 18.75,
        "ROE (Return on Equity) (%)": 10,
        "ROA (Return on Assets) (%)": 6.5,
        "Current Ratio": 1.8,
        "Debt to Equity Ratio": 0.25,
        "Location": "Chicago, IL",
        "CEO": "Bob Johnson",
        "Number of Employees": 2000
    },
    "Internal Data": {
        "Company Name": "RetailCo",
        "Industry": "Retail",
        "Market Capitalization": 2000,
        "Revenue (in millions)": 800,
        "EBITDA (in millions)": 150,
        "Net Income (in millions)": 40,
        "Debt (in millions)": 100,
        "Equity (in millions)": 400,
        "Enterprise Value (in millions)": 2100,
        "P/E Ratio": 20,
        "Revenue Growth Rate (%)": 8,
        "EBITDA Margin (%)": 18.75,
        "Net Income Margin (%)": 5.0,
        "ROE (Return on Equity) (%)": 10.0,
        "ROA (Return on Assets) (%)": 6.5,
        "Current Ratio": 1.8,
        "Debt to Equity Ratio": 0.25,
        "Location": "Chicago"
    },
    "Discrepancies": {
        "Debt (in millions)": {
            "Extracted": 110,
            "Internal": 100
        },
        "Location": {
            "Extracted": "Chicago, IL",
            "Internal": "Chicago"
        }
    },
    "Missing in Extracted Data": [
        "Net Income Margin (%)"
    ],
    "Missing in Internal Data": [
        "Number of Employees",
        "CEO"
    ]
}

strFileNotFoundError = "An error occurred: Cannot extract data. Invalid file provided."
