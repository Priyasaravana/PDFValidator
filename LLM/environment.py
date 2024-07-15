import os

# for Azure open AI LLMs
def setup_environment(api_key: str, api_endpoint: str, api_version: str):
    """
    Set up the environment variables for Azure OpenAI.
    
    Args:
    - api_key (str): API key for Azure OpenAI.

    """
    os.environ["AZURE_OPENAI_API_KEY"] = api_key
    os.environ["AZURE_OPENAI_ENDPOINT"] = api_endpoint
    os.environ["OPENAI_API_VERSION"] = api_version

# connect to open ai LLMs
def setup_environment(api_key: str):
    """
    Set up the environment variables for Azure OpenAI.
    
    Args:
    - api_key (str): API key for Azure OpenAI.

    """
    os.environ["OPENAI_API_KEY"] = api_key
