from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
import csv
import io
import re
import random
import logging

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    
    participants = []

    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            if 'name' in request.form and 'email' in request.form:
                name = request.form['name'].strip()
                email = request.form['email'].strip()
                if is_valid_email(email) and email not in [participant['email'] for participant in participants]:
                    participants.append({'name': name, 'email': email})
                    flash('Participant added successfully!', 'success')
                else:
                    flash('Email must be unique and valid.', 'error')
            return redirect(url_for('index'))
        return render_template('index.html', participants=participants)

    @app.route('/upload_csv', methods=['POST'])
    def upload_csv():
        if 'csv_file' in request.files:
            csv_file = request.files['csv_file']
            if csv_file.filename.endswith('.csv'):
                try:
                    csv_content = io.StringIO(csv_file.stream.read().decode('utf-8'))
                    reader = csv.DictReader(csv_content)
                    for row in reader:
                        name = row['Name'].strip()
                        email = row['Email'].strip()
                        if is_valid_email(email) and email not in [participant['email'] for participant in participants]:
                            participants.append({'name': name, 'email': email})
                    flash('CSV file processed successfully!', 'success')
                except Exception as e:
                    flash(f'Error processing CSV file: {str(e)}', 'error')
            else:
                flash('Please upload a valid CSV file.', 'error')
        return redirect(url_for('index'))

    @app.route('/remove', methods=['POST'])
    def remove():
        email_to_remove = request.form['email_to_remove']
        nonlocal participants
        participants = [participant for participant in participants if participant['email'] != email_to_remove]
        flash('Participant removed successfully.', 'success')
        return redirect(url_for('index'))

    @app.route('/process')
    def process():
        if participants:
            total = len(participants)
            return render_template('credentials.html', participants=participants, total=total)
        else:
            flash('Please add some participants first.', 'error')
            return redirect(url_for('index'))

    @app.route('/send_emails', methods=['POST'])
    def send_emails():
        email_address = request.form['email_address']
        email_password = request.form['email_password']
        
        if len(participants) < 2:
            flash('Need at least two participants to proceed.', 'error')
            return redirect(url_for('index'))

        # Randomize and assign Secret Santas
        shuffled = participants[:]
        random.shuffle(shuffled)
        pairs = list(zip(participants, shuffled))

        logging.debug(f"Pairs: {pairs}")

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.set_debuglevel(1)  # Enable smtplib debug output
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email_address, email_password)
            for gifter, receiver in pairs:
                msg = MIMEText(f"Dear {gifter['name']},\nYou have been assigned to be the Secret Santa for {receiver['name']}!")
                msg['Subject'] = 'Secret Santa'
                msg['From'] = email_address
                msg['To'] = gifter['email']
                logging.debug(f"Sending email to {gifter['email']} with message: {msg.as_string()}")
                server.sendmail(email_address, gifter['email'], msg.as_string())
            server.quit()
            flash('Emails sent successfully!', 'success')
        except smtplib.SMTPAuthenticationError:
            flash('Failed to send emails: Authentication error. Please check your email and password.', 'error')
        except smtplib.SMTPException as e:
            flash(f'Failed to send emails: {str(e)}', 'error')
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
