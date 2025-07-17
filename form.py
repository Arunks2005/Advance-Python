import streamlit as st

def main():
    st.title('Form Example')
    
    # Text input
    name = st.text_input('Enter your name')
    
    # Number input
    age = st.number_input('Enter your age', min_value=0, max_value=150)
    
    # Dropdown selection
    gender = st.selectbox('Select your gender', ['Male', 'Female', 'Other'])
    
    # Checkbox selection
    hobbies = st.multiselect('Select your hobbies', ['Reading', 'Gaming', 'Traveling'])
    
    # Button click
    if st.button('Submit'):
        st.write('Name:', name)
        st.write('Age:', age)
        st.write('Gender:', gender)
        st.write('Hobbies:', hobbies)

if __name__ == '__main__':
    main()
