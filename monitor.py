# import time
# import smtplib
# import socket
# import psutil
# import os
# from email.message import EmailMessage
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Gmail configuration
# GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
# GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
# TO_EMAIL = os.getenv("TO_EMAIL")

# # Thresholds
# CPU_THRESHOLD = 10         # Alert if CPU > 10%
# RAM_THRESHOLD = 10         # Alert if RAM > 10%
# DISK_THRESHOLD = 50        # Alert if less than 50% disk space free

# # Get system time and hostname
# current_time = time.localtime()
# formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
# hostname = socket.gethostname()

# def send_alert(subject, message):
#     email = EmailMessage()
#     email['From'] = GMAIL_ADDRESS
#     email['To'] = TO_EMAIL
#     email['Subject'] = subject

#     # Plain text fallback
#     email.set_content(message)

#     # HTML version
#     email.add_alternative(f"""\
#     <html>
#       <body>
#         <h2>System Alert from <b>{hostname}</b> - {formatted_time}</h2>
#         <pre style="font-size: 16px; font-family: monospace;">{message}</pre>
#       </body>
#     </html>
#     """, subtype='html')

#     try:
#         with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#             smtp.starttls()
#             smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
#             smtp.send_message(email)
#             print("✅ Gmail alert sent successfully.")
#     except Exception as e:
#         print(f"❌ Failed to send Gmail alert: {str(e)}")

#         # Optional: Log the error
#         with open("alerts.log", "a") as f:
#             f.write(f"{formatted_time} - ❌ Email Error: {str(e)}\n")

# # Monitor system metrics
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
#     subject = f"[{hostname}] Monitoring Alert - {formatted_time}"
#     send_alert(subject, alert_message)

#     # Optional: Log the alert locally
#     with open("alerts.log", "a") as f:
#         f.write(f"{formatted_time} - ALERT SENT\n{alert_message}\n\n")
# else:
#     print("✅ All system metrics are within normal limits.")


from dotenv import load_dotenv
load_dotenv()

import time
import os
from mailjet_rest import Client
import psutil

# Mailjet configuration
api_key = os.getenv('MAILJET_API_KEY')
api_secret = os.getenv('MAILJET_API_SECRET')

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

# Thresholds
CPU_THRESHOLD = 80     # percent
RAM_THRESHOLD = 80     # percent
DISK_THRESHOLD = 50    # percent free


def send_alert(subject, message):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "michael.lamptey@amalitechtraining.org",
                    "Name": "24/7 SysMon"
                },
                "To": [
                    {
                        "Email": "odarteilamptey.ml@gmail.com",
                        "Name": "Admin"
                    }
                ],
                "Subject": subject,
                "HTMLPart": f"<h3>{message}</h3>"
            }
        ]
    }

    try:
        result = mailjet.send.create(data=data)
        print(f"Email sent: {result.status_code}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


def monitor_system(cpu_threshold=CPU_THRESHOLD, memory_threshold=RAM_THRESHOLD, disk_threshold=DISK_THRESHOLD, interval=60):
    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_used = psutil.disk_usage('/').percent
        disk_free = 100 - disk_used

        print(f"[{current_time}] CPU: {cpu_usage}% | Memory: {memory_usage}% | Disk Free: {disk_free}%")

        if cpu_usage > cpu_threshold:
            send_alert("🚨 High CPU Usage Alert", f"CPU usage is at {cpu_usage}%, above threshold {cpu_threshold}%")

        if memory_usage > memory_threshold:
            send_alert("🚨 High Memory Usage Alert", f"Memory usage is at {memory_usage}%, above threshold {memory_threshold}%")

        if disk_free < disk_threshold:
            send_alert("🚨 Low Disk Space Alert", f"Disk free space is at {disk_free}%, below threshold {disk_threshold}%")

        time.sleep(interval)


if __name__ == "__main__":
    # Optional test email - uncomment to test
    # send_alert("✅ Mailjet Test Alert", "This is a test email from your Python monitoring script. If you see this, it worked!")

    # Start monitoring
    monitor_system()