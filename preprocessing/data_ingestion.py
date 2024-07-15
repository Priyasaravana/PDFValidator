import pandas as pd
from src.pdf_service import PdfService
from fastapi import HTTPException

def load_company_data(company_name, data_path):
    """
    Loads company data from a CSV file and returns a dictionary.

    Args:
        company_name (str): The name of the company to retrieve data for.
        data_path (str, optional): The path to the CSV file containing the data.
            Defaults to "data/database.csv".

    Returns:
        Dict: A dictionary containing company data based on the company_name,
            or "Data Not Found" if not found.
    """

    # Read the CSV data into a pandas DataFrame
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        return {"Company Name": "Data Not Found (File Error)"}

    # Select the row for the specified company name
    company_data = df[df["Company Name"] == company_name].to_dict("records")

    # Check if data was found for the company
    if company_data:
        # Return the first row (assuming unique company names)
        return company_data[0]
    else:
        return {"Company Name": "Data Not Found"}
    
def extract_PdfDetails(pdf_file_path):
    """Extracts details from a PDF file using PdfService.

    Args:
        pdf_file_path (str): The path to the PDF file.

    Returns:
        dict: The extracted data from the PDF.

    Raises:
        Exception: If an error occurs during PDF extraction.
    """

    extracted_data = PdfService(key="TEST_KEY").extract(pdf_file_path)  
    return extracted_data  

def extractDetails(pdf_file_path, database_path="data/database.csv"):
    """Extracts details from a PDF file and combines with internal data.

    Args:
        pdf_file_path (str): The path to the PDF file.
        database_path (str, optional): The path to the database CSV file. Defaults to "data/database.csv".

    Returns:
        tuple: A tuple containing extracted data, internal data, and company name.

    Raises:
        Exception: If an error occurs during PDF extraction or data loading.
    """

    # Call the external service (PdfService) to extract data from PDF
    extracted_data = extract_PdfDetails(pdf_file_path)  

    # Extract the company name
    company_name = extracted_data.get("Company Name")
    # Load data from internal storage (replace with your logic)
    internal_data = load_company_data(company_name, database_path)
    return extracted_data, internal_data, company_name

def compareData(extracted_data, internal_data):
    """Compares extracted and internal data, identifying discrepancies and missing fields.

    Args:
        extracted_data (dict): The data extracted from the PDF.
        internal_data (dict): The internal company data.

    Returns:
        dict: A dictionary containing extracted data, internal data, discrepancies, and missing fields.
    """
    
    # Prepare the response dictionary
    response = {
        "Extracted Data": extracted_data,
        "Internal Data": internal_data,
        "Discrepancies": {},
        "Missing in Extracted Data": [],
        "Missing in Internal Data": [],
    }

    extracted_data_fields = set(extracted_data.keys())
    internal_data_fields = set(internal_data.keys())

    missing_in_extracted = internal_data_fields - extracted_data_fields
    missing_in_internal = extracted_data_fields - internal_data_fields

    # Update the response dictionary with missing fields
    response["Missing in Extracted Data"] = list(missing_in_extracted)
    response["Missing in Internal Data"] = list(missing_in_internal)
    
    # Compare extracted and internal data, identify discrepancies
    for field, value in extracted_data.items():
        if field in internal_data and value != internal_data[field]:
            response["Discrepancies"][field] = {
                "Extracted": value,
                "Internal": internal_data.get(field, "Data Not Found"),
            }

    return response 
