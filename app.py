# cre by Daniel Klein 

import streamlit as st
from streamlit.session_state import SessionState
import firebase_admin
from firebase_admin import credentials, auth
from textblob import TextBlob
from auth import *

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return sentiment

# Initialize Firebase Admin SDK
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Function to register new users
def register():
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')
    
    if password != confirm_password:
        st.error('Passwords do not match.')
    elif st.button('Register'):
        try:
            user = auth.create_user(email=email, password=password)
            st.success(f'User {email} created successfully!')
        except:
            st.error('Error creating user.')


# Khởi tạo state để lưu lịch sử chat
state = SessionState(history=[])

# Tạo khung để hiển thị lịch sử chat
if st.button('Lịch sử chat'):
    for item in state.history:
        st.write(item['question'])
        st.write(item['answer'])

# Lưu câu hỏi và trả lời vào lịch sử chat
question = st.text_input('Nhập câu hỏi của bạn:')
if st.button('Gửi'):
    # Xử lý câu hỏi và trả lời tại đây
    answer = get_answer_from_openai(question)

    # Lưu vào lịch sử
    state.history.append({
        'question': question,
        'answer': answer
    })

    # Hiển thị câu trả lời
    st.write(answer)
# Tạo khung để hiển thị lịch sử chat và tìm kiếm
search_term = st.text_input('Tìm kiếm trong lịch sử:')
if st.button('Tìm kiếm'):
    results = []
    for item in state.history:
        if search_term.lower() in item['question'].lower() or search_term.lower() in item['answer'].lower():
            results.append(item)

    if len(results) == 0:
        st.write('Không tìm thấy kết quả nào.')
    else:
        for item in results:
            st.write(item['question'])
            st.write(item['answer'])



# Thêm phần logo
from PIL import Image
logo = Image.open("path/to/logo.png")
st.image(logo, use_column_width=True)

# Thêm phần giới thiệu
st.markdown(
"""
# Chào mừng bạn đến với DChatBot!

Bạn cảm thấy mệt mỏi khi phải vật lộn để tự viết code?
Đừng lo đã có DK ở đây! Mình sẽ là người giúp bạn viết code với nhiều ngôn ngữ lập trình khác. 
Cho dù bạn là nhà phát triển có nhiều kinh nghiệm hay mới bắt đầu, 
DChatBot là nơi hoàn hảo để nhận trợ giúp mà bạn cần.

Còn chờ gì nữa! Bắt đầu sử dụng DChatBot ngay và luôn.
""",
unsafe_allow_html=True)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

js = """
    function changeBackgroundColor() {
        var element = document.body;
        element.classList.toggle("dark-mode");
    }
"""
st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)



# Thêm khung chatbot
st.text_input("Hãy nhập câu hỏi của bạn tại đây:")
st.button("Gửi")

app = Flask(__name__)
openai.api_key = "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"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=(f"Q: {userText}\nA:"),
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return str(response.choices[0].text)

if __name__ == "__main__":
    app.run()
