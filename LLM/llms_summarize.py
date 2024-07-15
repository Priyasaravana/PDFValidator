import os
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from src.constants import api_key
from openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from LLM.llm_loader import initialize_llm
from LLM.chain import create_prompt_template, create_chain
from langchain_community.llms import Ollama
from LLM.environment import setup_environment

# Environment setup
setup_environment(
    api_key=api_key
    # ,
    # api_version = '2023-12-01-preview'
)
#OpenAI.api_key= api_key
#os.environ['OPENAI_API_KEY'] = OpenAI.api_key    
client = OpenAI()

#open AI and Langchain integration for summarization
def summarize_chain(dctSummarize, company_name):
    """Summarizes the given data using the Open AI LLM.

    Args:
        dctSummarize (dict): The data to be summarized.
        company_name (str): The company name.

    Returns:
        str: The summarized output.
    """
    # Define a template for the prompt
    prompt_template = prompttemplate2()
    # Specify input variables for the template
    input_variables = ["internal_data", "external_data", "discrepancy_fields", "missing_extracted_fields", "missing_internal_fields", "company name"]

    # Create the PromptTemplate instance
    prompt = PromptTemplate(input_variables=input_variables, template=prompt_template)

     # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    # Create the LLMChain with OpenAI LLM (replace if needed)
    # llm_chain = LLMChain(llm=llm, prompt=prompt, output_parser=StrOutputParser())

    data_with_prompt_data = extractPromptData(dctSummarize, company_name)
    
    chain = prompt | llm | StrOutputParser()

    # Run the LLM chain with prepared data
    summary = chain.invoke(data_with_prompt_data)
    return summary

#open AI and Langchain integration for summarization
def summarize_chain_betteralign(dctSummarize, company_name):
    """Summarizes the given data using the OpenAI LLM.

    Args:
        dctSummarize (dict): The data to be summarized.
        company_name (str): The company name.

    Returns:
        str: The summarized output.
    """
    # Define a template for the prompt with placeholders
    prompt_template = """Based on the analysis of financial data from two sources for {company_name}, the following key findings can be summarized regarding its financial health:

    {findings}

    Overall, the discrepancies and missing information in the financial data of {company_name} raise concerns about the accuracy, transparency, and completeness of the company's financial reporting. These gaps make it challenging to make a comprehensive assessment of {company_name}'s financial health.
    """

    # Specify input variables for the template
    input_variables = ["company_name", "findings"]

    # Create the PromptTemplate instance
    prompt = PromptTemplate(input_variables=input_variables, template=prompt_template)
    
    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

    findings_str = extractPromptdetails(dctSummarize)

    # Prepare data dictionary with company name and findings
    data = {
    "company_name": company_name,
    "findings": findings_str
    }

    chain = prompt | llm | StrOutputParser()

    # Run the LLM chain with prepared data
    summary = chain.invoke(data)
    print(summary)
    return summary

#Azure language model
def summarizeAzureOpenAI(dctSummarize, company_name):
    """Summarizes the given data using the Azure OpenAI LLM.

    Args:
        dctSummarize (dict): The data to be summarized.
        company_name (str): The company name.

    Returns:
        str: The summarized output.
    """
    llm = initialize_llm(deployment_name="ss-gpt-32k")
    # Create prompt template
    template = prompttemplate()
    prompt = create_prompt_template(template)
    chain = create_chain(prompt, llm)

    data_with_prompt_data = extractPromptData(dctSummarize, company_name)

    response = chain.invoke(data_with_prompt_data)
    return response

#Local language model 'OLLAMA' and Langchain integration for summarization
def OLLAMASummarization(dctSummarize, company_name):
    """Summarizes the given data using the local LLM 'LLAMA 8 B'.

    Args:
        dctSummarize (dict): The data to be summarized.
        company_name (str): The company name.

    Returns:
        str: The summarized output.
    """
    promp_template = prompttemplate()
    input_variables = ["internal_data", "external_data", "discrepancy_fields", "missing_extracted_fields", "missing_internal_fields", "company name"]

    # Create the PromptTemplate instance
    prompt = PromptTemplate(input_variables=input_variables, template=promp_template)
    llm = Ollama(model="llama3:8b")
    chain =  prompt | llm | StrOutputParser()
    data_with_prompt_data = extractPromptData(dctSummarize, company_name)
    summary = chain.invoke(data_with_prompt_data)
    
    return summary

def prompttemplate():
    template = """
        As a seasoned real-time fund and portfolio analyst at Lantern, you are tasked with providing in-depth analysis and summarization to enhance data source comparison check.
        You will be working with detailed fields that outline Internal data source, external data source, discrepancies in field and missing fields.
        Your objective is to leverage these elements to deliver robust, actionable insights and summary.
        Given Data Sources and discrepancy details:
        Internal Data:{internal_data}
        External Data:{external_data}
        * Discrepancies:
            * {discrepancy_fields}
        * Missing from Extracted Data:
            * {missing_extracted_fields}
        * Missing from Internal Data:
            * {missing_internal_fields}

        Evaluate and Summarize: Review the Internal data and external data to identify the fields and compare it with external data.

        Analyze Discrepancies: Examine the Discrepancies to understand the difference between the two sources. Assess the discreancies in values between the two sources and provide the details clearly to the customer.Summarize the key discrepancies that the impact of this could have on the system.
        Identify Missing Fields: Based on the Missing extracted field and Missinf Internal fields, determine if there are fields which miss between the two sources. Highlight the missing fields under the sources.
        Enhance summarization: Building on the provided details, summarize the details.

        Your Summarization should:

        - Be detailed and actionable, offering the details about the discrepancy and missing fields.
        - Reflect insights on the data to make actionble outcome in the field of real-time fund and portfolio analytics.

        Output Format:
        Please respond with comprehensive summarization in Markdown format.
        """
    return template

def prompttemplate2():
    prompt_template = """I analyzed financial data from two sources for the given {company_name} and found the following:
    Internal Data:{internal_data}
    External Data:{external_data}
    * Discrepancies:
        * {discrepancy_fields}
    * Missing from Extracted Data:
        * {missing_extracted_fields}
    * Missing from Internal Data:
        * {missing_internal_fields}

    Based on this information, can you summarize the key findings about {company_name} financial health?
    """
    return prompt_template

def extractPromptData(dctSummarize, company_name):
    """Extracts data for the prompt from the provided dictionary.

    Args:
        dctSummarize (dict): The dictionary containing the data.
        company_name (str): The company name.

    Returns:
        dict: A dictionary containing data for the prompt.
    """
    # Extract data for the prompt
    external_data = dctSummarize["Extracted Data"]
    internal_data = dctSummarize["Internal Data"]
    discrepancy_fields = ", ".join(dctSummarize["Discrepancies"].keys())
    missing_extracted_fields = ", ".join(dctSummarize["Missing in Extracted Data"])
    missing_internal_fields = ", ".join(dctSummarize["Missing in Internal Data"])

    # Prepare the data dictionary with extracted values
    data_with_prompt_data = {
    "external_data": external_data,
    "internal_data": internal_data, 
    "discrepancy_fields": discrepancy_fields,
    "missing_extracted_fields": missing_extracted_fields,
    "missing_internal_fields": missing_internal_fields,
    "company_name":company_name
    }
    return data_with_prompt_data

def extractPromptdetails(dctSummarize):
        # Construct the findings string dynamically based on data dictionary
    finding_lines = []
    for field, discrepancy in dctSummarize["Discrepancies"].items():
        extracted_value = dctSummarize["Extracted Data"][field]
        internal_value = dctSummarize["Internal Data"][field]
        finding_lines.append(f"\n* Discrepancy in {field}:")
        finding_lines.append(f"  * Extracted Data: {extracted_value}")
        finding_lines.append(f"  * Internal Data: {internal_value}")

    for missing_field in dctSummarize["Missing in Extracted Data"]:
        finding_lines.append(f"\n* Missing field in Extracted Data: {missing_field}")

    for missing_field in dctSummarize["Missing in Internal Data"]:
        finding_lines.append(f"\n* Missing field in Internal Data: {missing_field}")

    findings_str = "\n".join(finding_lines)
    return findings_str