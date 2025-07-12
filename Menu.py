import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import pywhatkit as kit
import time

# ========== 1. Web Scraping Function ==========
def web_scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("\n=== Page Title ===")
    print(soup.title.string)

# ========== 2. Send Email ==========
def send_email(sender_email, password, receiver_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
    print("Email sent successfully!")

# ========== 3. Send SMS ==========
def send_sms(account_sid, auth_token, from_num, to_num, message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=from_num,
        to=to_num
    )
    print("SMS sent! SID:", message.sid)

# ========== 4. Make Phone Call ==========
def make_call(account_sid, auth_token, from_num, to_num, twiml_url='http://demo.twilio.com/docs/voice.xml'):
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        twiml=f'<Response><Say>{twiml_url}</Say></Response>',
        to=to_num,
        from_=from_num
    )
    print("Call initiated! SID:", call.sid)

# ========== 5. Send WhatsApp Message ==========
def send_whatsapp_msg(phone_no, message, hour, minute):
    kit.sendwhatmsg(phone_no, message, hour, minute)
    print("WhatsApp message scheduled!")

# ========== MAIN MENU ==========
def main():
    while True:
        print("\n========= PYTHON AUTOMATION MENU =========")
        print("1. Web Scraping")
        print("2. Send Email")
        print("3. Send SMS")
        print("4. Make Phone Call")
        print("5. Send WhatsApp Message")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            url = input("Enter the URL to scrape: ")
            web_scrape(url)

        elif choice == '2':
            sender = input("Enter sender email: ")
            pwd = input("Enter email password (App password for Gmail): ")
            receiver = input("Enter receiver email: ")
            subject = input("Enter subject: ")
            body = input("Enter message body: ")
            send_email(sender, pwd, receiver, subject, body)

        elif choice == '3':
            sid = input("Enter Twilio SID: ")
            token = input("Enter Twilio Auth Token: ")
            from_num = input("Enter Twilio Phone Number: ")
            to_num = input("Enter Recipient Number: ")
            msg = input("Enter message: ")
            send_sms(sid, token, from_num, to_num, msg)

        elif choice == '4':
            sid = input("Enter Twilio SID: ")
            token = input("Enter Twilio Auth Token: ")
            from_num = input("Enter Twilio Phone Number: ")
            to_num = input("Enter Recipient Number: ")
            make_call(sid, token, from_num, to_num)

        elif choice == '5':
            phone = input("Enter WhatsApp number (with country code): ")
            message = input("Enter message: ")
            hour = int(input("Enter hour (24h format): "))
            minute = int(input("Enter minute: "))
            send_whatsapp_msg(phone, message, hour, minute)

        elif choice == '6':
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Try again!")

if __name__ == "__main__":
    main()
