import pyrebase

firebase_config = {
    "apiKey": "your_api_key",
    "authDomain": "your_auth_domain",
    "databaseURL": "your_database_url",
    "projectId": "your_project_id",
    "storageBucket": "your_storage_bucket",
    "messagingSenderId": "your_messaging_sender_id",
    "appId": "your_app_id",
    "measurementId": "your_measurement_id"
}

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()
db = firebase.database()


def register(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return True, user
    except:
        return False, None


def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return True, user
    except:
        return False, None
from auth import register, login

# sử dụng hàm register để đăng ký
success, user = register(email, password)

# sử dụng hàm login để đăng nhập
success, user = login(email, password)
login()
register()

