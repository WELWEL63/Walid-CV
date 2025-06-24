from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

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

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name', 'Email', 'Mobile', 'Subject', 'Message'])
        writer.writerow([name, email, mobile, subject, message])

    flash('Your message has been submitted successfully!')
    return redirect(url_for('home'))


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80)
   app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))  # Use port from Render



