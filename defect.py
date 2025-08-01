import os
import streamlit as st 
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

from PIL import Image # pillow is used to load,save and manipulate the image
st.set_page_config(page_title='Defect Detection',page_icon='🌐' ,layout='wide')

st.title('AI Assistant for :green[Structural defect and analysis]')
st.subheader(':blue[Prototype for automated structural analysis]',divider=True)

with st.expander('About the application'):
    st.markdown(f'''
                This prototype is used to detect the structural defects and analyse the 
                defects in the system using AI powered system. \n
                **Defect Detection**: Automatically detects the structural defects in the system \n
                **Recommendations**: Provides solutions and recommendations based on the defects \n
                **Report Generation**: Create a detailed report for the documentation and understanding \n
                ''')
    
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = key)

st.subheader('Upload image here')
input_image = st.file_uploader('Upload the image here',type=['png','jpg','jpeg'])
if input_image:
    img = Image.open(input_image)
    st.image(img,caption='Uploaded Image')

prompt = f'''
        context: I am trying to find the structural defect in the image. Help me find the defect in the image.
        for easier detection, most of the images provided are related to construction based structural defects.
        {input_image}
        '''
gemini_model = genai.GenerativeModel('gemini-2.0-flash')
response = gemini_model.generate_content(prompt)
st.markdown(':[Result]')
st.write(response.text)