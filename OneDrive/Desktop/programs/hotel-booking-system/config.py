import os

class Config:
    SECRET_KEY = "hotel_booking_secret_key"

    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "hotel_booking"

    UPLOAD_FOLDER = os.path.join("static", "uploads")