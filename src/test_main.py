# Write your tests here
import unittest
from unittest.mock import patch, MagicMock  # Mocking imports
from fastapi import FastAPI
from fastapi.testclient import TestClient  # Used for some tests
import pandas as pd
from main import app, load_company_data
from pdf_service import PdfService
from testMockValues import responseMockData, strFileNotFoundError
from sortedcontainers import SortedDict
from preprocessing.data_ingestion import load_company_data, extractDetails, compareData
import functools

# class TestAPI(unittest.TestCase):
#     def test_foo(self):
#         self.assertEqual('foo'.upper(), 'FOO')

client = TestClient(app) 


class TestAPI(unittest.TestCase):
    # def setUp(self):
    #     self.app = FastAPI()

    def compare_dicts_ignore_order(actual_data, expected_data):
        """
        Compares two dictionaries, ignoring order within nested structures.

        Args:
            actual_data: The actual dictionary to compare.
            expected_data: The expected dictionary to compare against.

        Returns:
            True if all keys and their corresponding values match, False otherwise.
        """
        actual_keys = set(actual_data.keys())
        expected_keys = set(expected_data.keys())

        # Check if all expected keys are present in actual data
        if not actual_keys >= expected_keys:
            return False

        # Compare values for matching keys
        for key in expected_keys:
            if actual_data[key] != expected_data[key]:
                return False

        return True
    
    def compare_data(self, strItemtoCompare, ItemType):
        """
        Tests successful data comparison for valid query parameters.

        Args:
            strItemtoCompare (str): The key within the response data to compare (e.g., "Extracted Data").
        """
        query_params  = {
            "pdf_file_path": "assets/retailco.pdf",
            "database_path": "data/database.csv"
        }

        # Send a GET request to the compare_data endpoint
        response = client.get("/compare_data", params=query_params)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the response data structure
        expected_response = responseMockData[strItemtoCompare]
 
        if ItemType == 'Dict':
            actual_data_sorted = SortedDict(response.json()[strItemtoCompare])
            expected_data_sorted = SortedDict(expected_response)
            return self.assertEqual(actual_data_sorted, expected_data_sorted)
        else:
            print(response.json()[strItemtoCompare])
            print(expected_response)
            return self.assertEqual(sorted(response.json()[strItemtoCompare]), sorted(expected_response))
        
         # Assert the response data structure
        
    
    #positive test scenario 1
    def test_read_root(self):

        """Tests the root endpoint (`/`) of the API."""
       
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    #positive test scenario 2
    def test_read_root_mock(self):
        with patch.object(FastAPI, '__init__'):  # Mock FastAPI initialization
            mocked_app = app  # Now a regular FastAPI instance

            @mocked_app.get("/")
            async def mock_root_endpoint():
                return {"Hello": "World"}

            with TestClient(mocked_app) as client:
                response = client.get("/")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"Hello": "World"})

    #positive test scenario 3
    def test_get_llm_response_success(self):
        """
        Tests successful LLM response generation for a valid PDF path.
        """

        query_params  = {
            "pdf_file_path": "assets/retailco.pdf",
            "database_path": "data/database.csv"
        }

        # Send a POST request to the compare_data endpoint
        response = client.get("/LLMResponse", params=query_params)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)
    
    #positive test scenario 4
    def test_compare_data_Expected_Data(self):
        """
        Tests successful data comparison for valid query parameters using "Extracted Data".
        """
        response = self.compare_data("Extracted Data", 'Dict')
        return response

    #positive test scenario 5 
    def test_compare_data_Internal_Data(self):
        """
        Tests successful data comparison for valid query parameters using "Internal Data".
        """
        response = self.compare_data("Internal Data", 'Dict')
        return response
    
    #positive test scenario 6
    def test_compare_data_Discrepancies_Data(self):
        """
        Tests successful data comparison for valid query parameters using "Discrepancies".
        """
        response = self.compare_data("Discrepancies", 'Dict')
        return response
    
    #positive test scenario 7
    def test_compare_data_MissExtract_Data(self):
        """
        Tests successful data comparison for valid query parameters using "Missing in Extracted Data".
        """
        response = self.compare_data("Missing in Extracted Data", 'List')
        return response
    
    #positive test scenario 8
    def test_compare_data_MissInternal_Data(self):
        """
        Tests successful data comparison for valid query parameters using "Missing in Extracted Data".
        """
        response = self.compare_data("Missing in Internal Data", 'List')
        return response
    
    #Negative test scenarios involve testing the system with invalid or unexpected inputs to ensure it handles errors gracefully
    #Negative test case 1
    # Send a GET request to Verify if the file data match
    # Invalid File path
    def test_file_not_match(self):
        """
        Tests successful data comparison for valid query parameters using "Missing in Extracted Data".
        """
        query_params  = {
            "pdf_file_path": "assets/retalco.pdf" #spelled wrongly
        }
        response = client.get("/extractPdfData", params=query_params)

        # Assert the response status code
        self.assertEqual(response.status_code, 500)

        # Assert the response data structure
        expected_response = strFileNotFoundError
        self.assertEqual(expected_response, response.json()["detail"])

    #Negative test case 2
    # Without sending query parameter details
    def test_extract_pdf_data_missing_parameter(self):
        response = client.get("/extractPdfData")
        self.assertEqual(response.status_code, 422) 

    #Negative test case 3
    # Sending invalid pdf file path
    def test_extract_pdf_data_invalid_path(self):
        response = client.get("/extractPdfData", params={"pdf_file_path": "invalid/path/to/pdf.pdf"})
        self.assertEqual(response.status_code, 500)       

    #Negative test case 4
    def test_compare_data_invalid_paths(self):
        response = client.get("/compare_data", params={"pdf_file_path": "invalid/path/to/pdf.pdf", "database_path": "invalid/path/to/database.csv"})
        self.assertEqual(response.status_code, 500)
        self.assertIn("An error occurred", response.json()["detail"])

    #Negative test case 5
    def test_compare_data_missing_parameters(self):
        response = client.get("/compare_data", params={"pdf_file_path": "assets/retailco.pdf"})
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity due to missing required query parameter

    #Negative test case 6
    def test_llm_response_invalid_paths(self):
        response = client.get("/LLMResponse", params={"pdf_file_path": "invalid/path/to/pdf.pdf", "database_path": "invalid/path/to/database.csv"})
        self.assertEqual(response.status_code, 500)
        self.assertIn("An error occurred", response.json()["detail"])

    #Negative test case 7
    def test_llm_response_missing_parameters(self):
        response = client.get("/LLMResponse", params={"pdf_file_path": "assets/retailco.pdf"})
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity due to missing required query parameter
    

if __name__ == "__main__":
    unittest.main()
