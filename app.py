import streamlit as st
import pandas as pd
from utils import get_recommendations  # Assuming get_recommendations function is in utils.py

st.set_page_config(page_title="Product Recommendation System", layout="wide")

st.markdown("<h1 style='text-align: center; color: maroon;'> TRIPATHI UTKARSH Product Recommendation </h1>", unsafe_allow_html=True)

user_query = st.text_input("Enter product details to get recommendations:")

if st.button(label="Get Recommendations") and user_query:
    recommendations = get_recommendations(user_query=user_query)

    num_products = len(recommendations)
    
    num_cols = 4
    num_rows = (num_products + num_cols - 1) // num_cols
    
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            idx = row * num_cols + col
            if idx < num_products:
                product = recommendations.iloc[idx]
                with cols[col]:
                    st.image(product['Image'], use_column_width=True)
                    st.write(f"**Product Name:** {product['Product Name']}")
                    st.write(f"**Similarity:** {(product['similarity'])*100:.2f}")
                    st.write(f"**Price:** {product['Price']}")
                    st.markdown(f"[Link]({product['Link']})", unsafe_allow_html=True)
