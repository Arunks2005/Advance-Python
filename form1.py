import streamlit as st
from PIL import Image

def main():
    st.title('Welcome to My Image Viewer!')
    st.write('Here is your image:')

    # Load and display image
    image = Image.open('profile.jpg')  # Replace with your image path
    st.image(image, caption='Your Image', use_column_width=True)

if __name__ == '__main__':
    main()
