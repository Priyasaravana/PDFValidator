from fastapi import FastAPI, UploadFile, Form, HTTPException, Query
from typing import Dict
from pydantic import BaseModel
from pdf_service import PdfService
from preprocessing.data_ingestion import load_company_data, extractDetails, compareData, extract_PdfDetails
import pandas as pd
import uvicorn
from llmModuleConnectors import LLMConnect

# Create an instance of PdfService to extract the information from the PDF
pdf_service = PdfService(key="TEST_KEY")
app = FastAPI()

@app.get("/")
async def read_root():
    """
    Root endpoint returning a simple message.
    """
    return {"Hello": "World"}

@app.get("/extractPdfData")
async def extract_PdfData(
    pdf_file_path: str = Query(..., description="Path to the uploaded PDF file")
) -> Dict:
    """
    Compares data extracted from PDF with existing company data.

    Args:
        pdf_file_path (str): The path to the uploaded PDF file.

    Returns:
        Dict: A dictionary containing the extracted data, internal data, and discrepancies.
    Raises:
        HTTPException: If there's an error during PDF extraction or data comparison.
    """
    try:
        extracted_data = extract_PdfDetails(pdf_file_path)   
        return extracted_data     
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/compare_data")
async def compare_data(
    pdf_file_path: str = Query(..., description="Path to the uploaded PDF file"),
    database_path: str = Query(..., description="Path to the database file")
) -> Dict:
    """
    Compares data extracted from PDF with existing company data.

    Args:
        pdf_file_path (str): The path to the uploaded PDF file.
        database_path (str): The path to the database file.

    Returns:
        Dict: A dictionary containing the extracted data, internal data, and discrepancies.
    Raises:
        HTTPException: If there's an error during PDF extraction or data comparison.
    """
    try:
        extracted_data, internal_data, company_name = extractDetails(pdf_file_path,  database_path)
        response = compareData(extracted_data, internal_data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/LLMResponse")
def getLLMresponse(
    pdf_file_path: str = Query(..., description="Path to the uploaded PDF file"),
    database_path: str = Query(..., description="Path to the database file")
) -> str:    
    """
    Generates LLM response based on extracted data.

    Args:
        pdf_file_path (str): The path to the PDF file (currently hardcoded).
        database_path (str): The path to the database file.

    Returns:
        Str: The LLM response.

    Raises:
        HTTPException: If there's an error during PDF extraction or data comparison.
    """
    try:
        extracted_data, internal_data, company_name = extractDetails(pdf_file_path, database_path)
        response = compareData(extracted_data, internal_data)
        output = LLMConnect.fnLLMConnect(response, company_name)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/LLMOpenAIResponse")
def getLLMresponse(
    pdf_file_path: str = Query(..., description="Path to the uploaded PDF file"),
    database_path: str = Query(..., description="Path to the database file")
) -> str:    
    """
    Generates LLM response based on extracted data.

    Args:
        pdf_file_path (str): The path to the PDF file (currently hardcoded).
        database_path (str): The path to the database file.

    Returns:
        Str: The LLM response.

    Raises:
        HTTPException: If there's an error during PDF extraction or data comparison.
    """
    try:
        extracted_data, internal_data, company_name = extractDetails(pdf_file_path, database_path)
        response = compareData(extracted_data, internal_data)
        output = LLMConnect.fnLLMConnect2(response, company_name)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
# Need to pass the Azure Open AI Key, Endpoint, API version
@app.get("/LLMAzureOpenAIResponse")
def getLLMresponse(
    pdf_file_path: str = Query(..., description="Path to the uploaded PDF file"),
    database_path: str = Query(..., description="Path to the database file")
) -> str:    
    """
    Generates LLM response based on extracted data.

    Args:
        pdf_file_path (str): The path to the PDF file (currently hardcoded).
        database_path (str): The path to the database file.

    Returns:
        Str: The LLM response.

    Raises:
        HTTPException: If there's an error during PDF extraction or data comparison.
    """
    try:
        extracted_data, internal_data, company_name = extractDetails(pdf_file_path, database_path)
        response = compareData(extracted_data, internal_data)
        output = LLMConnect.fnLLMLangChainConnect(response, company_name)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@app.get("/LLMOllamaResponse")
def getLLMresponse(
    pdf_file_path: str = Query(..., description="Path to the uploaded PDF file"),
    database_path: str = Query(..., description="Path to the database file")
) -> str:    
    """
    Generates LLM response based on extracted data.

    Args:
        pdf_file_path (str): The path to the PDF file (currently hardcoded).
        database_path (str): The path to the database file.

    Returns:
        Str: The LLM response.

    Raises:
        HTTPException: If there's an error during PDF extraction or data comparison.
    """
    try:
        extracted_data, internal_data, company_name = extractDetails(pdf_file_path, database_path)
        response = compareData(extracted_data, internal_data)
        output = LLMConnect.fnLLMOllamaConnect(response, company_name)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
# Run the application 
if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    extracted_data, internal_data, company_name = extractDetails(pdf_file_path='assets/retailco.pdf', database_path = 'data/database.csv')
    response = compareData(extracted_data, internal_data)
    output = LLMConnect.fnLLMOllamaConnect(response, company_name)
    print(output)

