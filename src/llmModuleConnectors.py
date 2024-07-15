from constants import api_key
from LLM.llms_summarize import summarize_chain, summarize_chain_betteralign, summarizeAzureOpenAI, OLLAMASummarization

class LLMConnect:
    """
    A class encapsulating different LLM connection methods.
    """
    
    #open AI API connect
    def fnLLMConnect(response, company_name): 
        """
        Summarizes the response using the summarize_chain_betteralign function.

        Args:
            response: The input data to be summarized.
            company_name: The name of the company.

        Returns:
            The summarized output.
        """
        output = summarize_chain_betteralign(response, company_name)
        return output
    
    def fnLLMConnect2(response, company_name):
        """
        Summarizes the response using the summarize_chain function.

        Args:
            response: The input data to be summarized.
            company_name: The name of the company.

        Returns:
            The summarized output.
        """
        output = summarize_chain(response, company_name)
        return output
    
    #AzureOpenAI deployed model API connect
    def fnLLMLangChainConnect(response, company_name):
        """
        Summarizes the response using the summarizeAzureOpenAI function.

        Args:
            response: The input data to be summarized.
            company_name: The name of the company.

        Returns:
            The summarized output.
        """
        output = summarizeAzureOpenAI(response, company_name)
        return output
    
    def fnLLMOllamaConnect(response, company_name):
        """
        Summarizes the response using the OLLAMASummarization function.

        Args:
            response: The input data to be summarized.
            company_name: The name of the company.

        Returns:
            The summarized output.
        """
        output = OLLAMASummarization(response, company_name)
        return output