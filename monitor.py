# import time
# import requests
# import smtplib
# from email.message import EmailMessage
# import psutil
# import os
# from dotenv import load_dotenv

# load_dotenv() 

# # api_key = os.getenv("MJ_APIKEY_PUBLIC")
# # api_secret = os.getenv("MJ_APIKEY_PRIVATE")

# # EMAILJS_SERVICE_ID = os.getenv("EMAILJS_SERVICE_ID")
# # EMAILJS_TEMPLATE_ID = os.getenv("EMAILJS_TEMPLATE_ID")
# # EMAILJS_USER_ID = os.getenv("EMAILJS_USER_ID")  # or EMAILJS_PUBLIC_KEY

# GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
# GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
# TO_EMAIL = os.getenv("TO_EMAIL")

# current_time = time.localtime()
# formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)

# CPU_THRESHOLD = 10         # Example: Alert if CPU > 10%
# RAM_THRESHOLD = 10         # Alert if RAM > 10%
# DISK_THRESHOLD = 50        # Alert if less than 50% disk space free

# # def send_alert(subject, message):
# #     mailjet = Client(auth=(api_key, api_secret), version='v3.1')
# #     data = {
# #         'Messages': [
# #             {
# #                 "From": {
# #                     "Email": "odarteilamptey.ml@gmail.com",
# #                     "Name": "24/7 SysMon"
# #                 },
# #                 "To": [
# #                     {
# #                         "Email": "odarteilamptey.ml@gmail.com",
# #                         "Name": "Admin"
# #                     }
# #                 ],
# #                 "Subject": subject,
# #                 "HTMLPart": f"<h3>{message}</h3>"
# #             }
# #         ]
# #     }
# #     try:
# #         result = mailjet.send.create(data=data)
# #         print(f"Email sent: {result.status_code}")
# #     except Exception as e:
# #         print(f"Failed to send email: {str(e)}")

# # def send_alert(subject, message):
# #     payload = {
# #         'service_id': EMAILJS_SERVICE_ID,
# #         'template_id': EMAILJS_TEMPLATE_ID,
# #         'user_id': EMAILJS_USER_ID,
# #         'template_params': {
# #             'subject': subject,
# #             'message': message,
# #             'timestamp': formatted_time
# #         }
# #     }

# #     try:
# #         response = requests.post('https://api.emailjs.com/api/v1.0/email/send', json=payload)
# #         print(f"Email status: {response.status_code}")
# #         if response.status_code == 200:
# #             print("✅ Alert email sent successfully.")
# #         else:
# #             print("⚠️ Failed to send email:", response.text)
# #     except Exception as e:
# #         print(f"❌ Exception occurred: {str(e)}")

# def send_alert(subject, message):
#     email = EmailMessage()
#     email['From'] = GMAIL_ADDRESS
#     email['To'] = TO_EMAIL
#     email['Subject'] = subject
#     email.set_content(message)

#     try:
#         with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#             smtp.starttls()
#             smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
#             smtp.send_message(email)
#             print("✅ Gmail alert sent successfully.")
#     except Exception as e:
#         print(f"❌ Failed to send Gmail alert: {str(e)}")



# cpu_usage = psutil.cpu_percent(interval=1)
# ram_usage = psutil.virtual_memory().percent
# disk_usage = psutil.disk_usage('/').percent


# alert_message = ""

# if cpu_usage > CPU_THRESHOLD:
#     alert_message += f"⚠️ CPU usage is high: {cpu_usage}% (Threshold: {CPU_THRESHOLD}%)\n"

# if ram_usage > RAM_THRESHOLD:
#     alert_message += f"⚠️ RAM usage is high: {ram_usage}% (Threshold: {RAM_THRESHOLD}%)\n"

# if disk_usage > DISK_THRESHOLD:
#     alert_message += f"⚠️ Low disk space: {100 - disk_usage}% free (Threshold: {DISK_THRESHOLD}% free)\n"

# if alert_message:
#     send_alert(f"Python Monitoring Alert - {formatted_time}", alert_message)
# else:
#     print("✅ All system metrics are within normal limits.")


import time
import smtplib
import socket
import psutil
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gmail configuration
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

# Thresholds
CPU_THRESHOLD = 10         # Alert if CPU > 10%
RAM_THRESHOLD = 10         # Alert if RAM > 10%
DISK_THRESHOLD = 50        # Alert if less than 50% disk space free

# Get system time and hostname
current_time = time.localtime()
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
hostname = socket.gethostname()

def send_alert(subject, message):
    email = EmailMessage()
    email['From'] = GMAIL_ADDRESS
    email['To'] = TO_EMAIL
    email['Subject'] = subject

    # Plain text fallback
    email.set_content(message)

    # HTML version
    email.add_alternative(f"""\
    <html>
      <body>
        <h2>System Alert from <b>{hostname}</b> - {formatted_time}</h2>
        <pre style="font-size: 16px; font-family: monospace;">{message}</pre>
      </body>
    </html>
    """, subtype='html')

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            smtp.send_message(email)
            print("✅ Gmail alert sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send Gmail alert: {str(e)}")

        # Optional: Log the error
        with open("alerts.log", "a") as f:
            f.write(f"{formatted_time} - ❌ Email Error: {str(e)}\n")

# Monitor system metrics
cpu_usage = psutil.cpu_percent(interval=1)
ram_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent

alert_message = ""

if cpu_usage > CPU_THRESHOLD:
    alert_message += f"⚠️ CPU usage is high: {cpu_usage}% (Threshold: {CPU_THRESHOLD}%)\n"

if ram_usage > RAM_THRESHOLD:
    alert_message += f"⚠️ RAM usage is high: {ram_usage}% (Threshold: {RAM_THRESHOLD}%)\n"

if disk_usage > DISK_THRESHOLD:
    alert_message += f"⚠️ Low disk space: {100 - disk_usage}% free (Threshold: {DISK_THRESHOLD}% free)\n"

if alert_message:
    subject = f"[{hostname}] Monitoring Alert - {formatted_time}"
    send_alert(subject, alert_message)

    # Optional: Log the alert locally
    with open("alerts.log", "a") as f:
        f.write(f"{formatted_time} - ALERT SENT\n{alert_message}\n\n")
else:
    print("✅ All system metrics are within normal limits.")
