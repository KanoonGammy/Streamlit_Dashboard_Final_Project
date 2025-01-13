import time
import os
import joblib # ไว้เซฟข้อมูลทั้งหมดที่เราพิมพ์
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY') #ไฟล์นามสกุล env
genai.configure(api_key=GOOGLE_API_KEY)

new_chat_id = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d-%Hh-%Mm-%Ss")
st.session_state.chat_id = new_chat_id
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '🐯'

# Create a data/ folder if it doesn't already exist
try:
    os.mkdir('data/')
except:
    # data/ folder already exists
    pass

# Load past chats (if available)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}

    st.session_state.chat_title = f'Task-{st.session_state.chat_id}'
    from io import StringIO
    import pathlib
    
    #upload file
    # uploaded_file = st.file_uploader("Upload a CSV file") # อัพโหลดข้อมูล
    bytes_data: bytes = None # กำหนดค่าเริ่มต้นก่อนเก็บเป็น byte
     # เลือก Model
    
    from PIL import Image
    import io
    import pandas as pd
        
    csv_data = pd.read_csv("datasource_for_AI.csv")
@st.cache_data
def AI_Overviews(prompt, data_csv, stock_name):
        # st.write(f"MIME type: {uploaded_file.type}")    
        st.session_state.model = genai.GenerativeModel('gemini-1.5-flash')
        csv_data = data_csv

        # st.write(csv_data)
        # csv_data = csv_data[csv_data['Name'] == stock_name]
        # st.write(csv_data)
        if stock_name != "":
            helper = csv_data[csv_data["Name"] == stock_name]["sector"].values[0]
            helper2 = csv_data[csv_data["Name"] == stock_name]["market"].values[0]
            csv_data = csv_data[(csv_data["market"] == helper2) & (csv_data["sector"] == helper)]
            st.success(f"กำลังวิเคราะห์หุ้น: {stock_name}")
        st.session_state.uploaded_csv = csv_data.to_csv(index = False)
        if stock_name in csv_data['Name'].values:

            csv_response = st.session_state.model.generate_content(
                [prompt, st.session_state.uploaded_csv]) 
            st.write(csv_response.text)

        else:
            if stock_name != "":
                st.error("ไม่พบหุ้นที่คุณกรอกในข้อมูล")
            else:
                pass


        