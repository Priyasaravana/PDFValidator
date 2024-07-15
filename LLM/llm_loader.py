from langchain_openai import AzureChatOpenAI

def initialize_llm(deployment_name: str) -> AzureChatOpenAI:
    """
    Initialize the AzureChatOpenAI model.
    
    Args:
    - deployment_name (str): The name of the deployment to use.
    
    Returns:
    - llm (AzureChatOpenAI): An initialized AzureChatOpenAI model.
    """
    return AzureChatOpenAI(deployment_name=deployment_name)
