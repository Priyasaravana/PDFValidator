import pandas as pd
import re

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the data by handling missing values and normalizing text fields.
    
    Args:
    - df (DataFrame): Input DataFrame to preprocess.
    
    Returns:
    - DataFrame: Preprocessed DataFrame.
    """
    df.fillna('N/A', inplace=True)

    def clean_text(text):
        if isinstance(text, str):
            text = text.upper()
            text = re.sub(r'[^\w\s]', '', text)
            text = text.strip()
        return text

    text_columns = ['Company Name', 'Industry', 'Location']
    for col in text_columns:
        df[col] = df[col].apply(clean_text)

    print("Data Preprocessing Complete. Here are the first few rows after preprocessing:")
    print(df.head())  
    return df
