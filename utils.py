import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

embedding = OpenAIEmbeddings()

dd = pd.read_parquet("patanjali_parquet_file.parquet")

def convert_to_array(x):
    try:
        if isinstance(x, str):
            x = eval(x)  
        return np.array(x, dtype=float)
    except (ValueError, SyntaxError, TypeError) as e:
        print(f"Error converting to array: {e}")
        return np.zeros((1,)) 

def get_recommendations(user_query, df=dd, embedding=embedding):

    user_embedding = np.array(embedding.embed_query(user_query))
    df['embeddings'] = df['embeddings'].apply(convert_to_array)

    if not all(isinstance(e, np.ndarray) for e in df['embeddings']):
        raise ValueError("Not all embeddings are valid numpy arrays.")

    df['similarity'] = df['embeddings'].apply(lambda x: cosine_similarity([user_embedding], [x])[0][0])
    recommended_products = df.sort_values(by='similarity', ascending=False)
    top_recommendations = recommended_products[['Product Name', 'similarity', 'Link', 'Price', 'Image']].head(10)
    
    return top_recommendations
