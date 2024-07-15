# PDFValidator
Multi-Source Data Summarization with Large Language Models
This project explores the use of Large Language Models (LLMs) to summarize key findings from comparing data from two different sources.

Project Overview

The project leverages various LLMs, including OpenAI, OLLAMA, and Azure OpenAI, for text summarization. It utilizes FastAPI to expose functionalities as an API.
The code prioritizes modularity and allows for easy extension and deployment.

Functionality:

Exploratory Data Analysis (EDA):
Analyzes input data using pandas and Plotly Express.
Performs tasks like data loading, cleaning, and visualization.

Data Source Comparison:
Compares data from two sources using APIs (steps not currently shown).

LLM-based Summarization:
Options to leverage both closed-source (OpenAI) and open-source (OLLAMA) LLMs.
Integrates with Azure OpenAI for deployed models.

API Testing:
Employs unit tests to ensure API functionality.

Project Structure:
The project follows a modular structure with the following key components:
Data Module: Handles data ingestion, storage, and retrieval (e.g., database.csv).
LLM Module: Manages LLM interaction (OpenAI, OLLAMA, Azure OpenAI) (e.g., environment.py, llm_loader.py).
Preprocessing Module: Prepares data for LLM analysis (e.g., data_ingestion.py, data_preprocessing.py).
Src Module: Exposes functionalities as an API using FastAPI (e.g., constants.py, main.py).
Util Module: Provides utility functions like logging (e.g., logger.py).

Deployment Options:
Manual Deployment: Install dependencies, configure credentials, and run the application.
Dockerized Deployment: Build a Docker image for wider distribution and cloud deployment.

Security Considerations:
Securely store API keys using environment variables or configuration management tools.
Implement access controls and data privacy practices.

Scalability and Extensibility:
Modular design facilitates component replacement and extension.
Cloud integration allows for scalability.
Reporting module can be extended for further visualization options.

Next Steps:
Implement the data source comparison functionality.
Integrate selected LLM model(s) for summarization.
Refine deployment options based on user needs.

For a more detailed understanding of specific functionalities, please refer to the corresponding code sections.
