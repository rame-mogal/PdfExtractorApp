import os
import openai
from dotenv import load_dotenv
import streamlit as st


load_dotenv()
openai.api_key = st.secrets["OPENAI_API_KEY"]

def query_openai_json(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1024,
        )
        return response.choices[0].message.content  # still a string
    except Exception as e:
        st.error(f"OpenAI API Error: {e}")
        return None
