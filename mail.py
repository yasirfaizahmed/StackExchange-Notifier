import smtplib
from email.mime.text import MIMEText
import os


def compose_email(date: str, message: str):
  email_text = f"""

  Date: {date}

  {message}

  """
  GMAIL_USERNAME = os.environ.get('FROM_MAIL')   # "professorsnipexd@gmail.com"
  GMAIL_APP_PASSWORD = os.environ.get('APP_PASSWORD')  # "xrwiszrvgqbpjvpm"

  recipients = ["{}".format(os.environ.get('TO_MAIL'))]
  msg = MIMEText(email_text)
  msg["Subject"] = "Email report: a simple sum"
  msg["To"] = ", ".join(recipients)
  msg["From"] = f"{GMAIL_USERNAME}@gmail.com"

  smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
  smtp_server.login(GMAIL_USERNAME, GMAIL_APP_PASSWORD)
  smtp_server.sendmail(msg["From"], recipients, msg.as_string())
  smtp_server.quit()
