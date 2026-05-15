import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from dotenv import load_dotenv

from gene_essence_engine.utils.write_progress import write_progress

if getattr(sys, 'frozen', False):
    load_dotenv(os.path.join(sys._MEIPASS, '.env'))
else:
    load_dotenv()


def send_email(to_email, attachment_path, log_callback=None):
    sender_address = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_PASSWORD')

    if not sender_address or not password:
        write_progress("[ERROR] Email credentials not configured. Check .env file.", callback=log_callback)
        return

    msg = MIMEMultipart()
    msg['From'] = sender_address
    msg['To'] = to_email
    msg['Subject'] = "Your Project Results – GeneEssenceGUI"

    mail_content = """\
Dear Researcher,

The results of your analysis are now available and can be found in the attachments to this email.

Thank you for using the GeneEssenceGUI!

We are available for any questions or support you may need.

Sincerely,
The Development Team – EngBIO
https://www.engbio.ufpa.br/
"""

    msg.attach(MIMEText(mail_content, 'plain'))

    filename = os.path.basename(attachment_path)

    try:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)
        write_progress("File successfully attached.", callback=log_callback)
    except FileNotFoundError:
        write_progress("[ERROR] The file was not found.", callback=log_callback)
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_address, password)
            server.sendmail(sender_address, to_email, msg.as_string())
        write_progress(f"Email with attachment successfully sent to {to_email}", callback=log_callback)
    except Exception as e:
        write_progress(f"[ERROR] Error sending email: {e}", callback=log_callback)