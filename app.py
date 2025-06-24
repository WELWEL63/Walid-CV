from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = 'your_secret_key'

CSV_FILE = 'contact_submissions.csv'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('Mobile')
    subject = request.form.get('subject')
    message = request.form.get('message')

    # Save to CSV
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name', 'Email', 'Mobile', 'Subject', 'Message'])
        writer.writerow([name, email, mobile, subject, message])

    # Send to Gmail
    try:
        send_email_to_gmail(name, email, mobile, subject, message)
        flash('Your message has been submitted and emailed successfully!')
    except Exception as e:
        print(f"Email sending failed: {e}")
        flash('Message saved, but failed to send email.')

    return redirect(url_for('home'))

def send_email_to_gmail(name, email, mobile, subject, message):
    msg = EmailMessage()
    msg['Subject'] = f'Contact Form Submission: {subject}'
    msg['From'] = 'redseaegypt24@gmail.com'
    msg['To'] = 'redseaegypt24@gmail.com'

    msg.set_content(f'''
New Contact Form Submission:

Name: {name}
Email: {email}
Mobile: {mobile}
Subject: {subject}
Message:
{message}
''')

    # Gmail SMTP settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    gmail_user = 'redseaegypt24@gmail.com'
    gmail_pass = 'nvpvmlraygcibnpt'  # Gmail app password

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
        smtp.login(gmail_user, gmail_pass)
        smtp.send_message(msg)

        
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80)
   app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))  # Use port from Render

