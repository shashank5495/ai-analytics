import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Analytics", layout="wide")

st.title("📊 Aroma House AI Analytics")

# Input box
question = st.text_input("Ask your question:")

if st.button("Run Query"):

    if question:
        with st.spinner("Generating response..."):

            response = requests.post(
                "http://127.0.0.1:8000/query",
                json={"question": question}
            )

            data = response.json()

            if "message" in data:
                st.warning(data["message"])

            elif "error" in data:
                st.error(data["error"])

            else:
                st.subheader("Generated SQL")
                st.code(data["sql"], language="sql")

                st.subheader("Result")
                df = pd.DataFrame(
                    data["result"]["rows"],
                    columns=data["result"]["columns"]
                )
                st.dataframe(df)

    else:
        st.warning("Please enter a question")