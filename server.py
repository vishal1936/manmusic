from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

app = Flask(__name__)

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_email(to_email, otp):
    from_email = "youremail@example.com"
    from_password = "yourpassword"

    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    your_email = data['yourEmail']
    other_email = data['otherEmail']
    
    otp = generate_otp()
    if send_email(other_email, otp):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)
