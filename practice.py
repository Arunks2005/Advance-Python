import streamlit as st
import pandas as pd

def main():
    st.title("User Details Form")

    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=0, max_value=120)
    email = st.text_input("Enter your email")
    country = st.selectbox("Select your country", ["India", "USA", "UK", "Germany", "Other"])

    if st.button("Submit"):
        data = {
            "Name": [name],
            "Age": [age],
            "Email": [email],
            "Country": [country]
        }
        df = pd.DataFrame(data)
        
        st.success("Submitted successfully!")
        st.write("### Entered Details")
        st.table(df)

if __name__ == '__main__':
    main()
