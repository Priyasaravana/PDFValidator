from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

def create_prompt_template(template: str) -> ChatPromptTemplate:
    """
    Create a chat prompt template.
    
    Args:
    - template (str): The template string to use for the prompt.
    
    Returns:
    - prompt (ChatPromptTemplate): A ChatPromptTemplate object.
    """
    return ChatPromptTemplate.from_template(template)

def create_chain(prompt: ChatPromptTemplate, llm: AzureChatOpenAI) -> object:
    """
    Create a chain with the prompt and LLM.
    
    Args:
    - prompt (ChatPromptTemplate): The prompt template to use.
    - llm (AzureChatOpenAI): The LLM to use.
    
    Returns:
    - chain (object): A processing chain.
    """
    return prompt | llm | StrOutputParser()
