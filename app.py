import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database Credentials (Aiven.io)
DB_CONFIG = {
    'host': 'YOUR_HOST',
    'user': 'YOUR_USER',
    'password': 'YOUR_PASSWORD',
    'database': 'defaultdb',
    'port': 12345
}

# Gmail SMTP Config
GMAIL_USER = 'your-email@gmail.com'
GMAIL_APP_PASS = 'xxxx-xxxx-xxxx-xxxx' # 16-character App Password

def send_mail(to_email, name):
    body = f"Hi {name},\n\nYour registration for WE-ICT 2026 is confirmed!\n\nLocation: BUET\nDate: TBA"
    msg = MIMEText(body)
    msg['Subject'] = 'Registration Confirmed - WE-ICT 2026'
    msg['From'] = GMAIL_USER
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASS)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO registrations (full_name, email, phone, institution, topic) VALUES (%s, %s, %s, %s, %s)",
                       (data['name'], data['email'], data['phone'], data['institution'], data['topic']))
        conn.commit()
        send_mail(data['email'], data['name'])
        return jsonify({"message": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run()
