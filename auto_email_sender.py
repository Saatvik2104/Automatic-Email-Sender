import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import tkinter as tk
from tkinter import filedialog

def choose_files():
    root = tk.Tk()
    root.attributes('-topmost', True)   
    root.iconify()                      
    file_paths = filedialog.askopenfilenames(
        title="Select files to attach",
        parent=root
    )
    root.destroy()                      
    return list(file_paths)

def get_smtp_settings(email):
    domain = email.split('@')[-1].lower()
    if 'gmail' in domain:
        return 'smtp.gmail.com', 587
    elif 'outlook' in domain or 'hotmail' in domain or 'live' in domain:
        return 'smtp.office365.com', 587
    elif 'yahoo' in domain:
        return 'smtp.mail.yahoo.com', 587
    else:
        print("Could not detect SMTP server for this email domain.")
        smtp_server = input("Enter SMTP server address (e.g., smtp.example.com): ")
        port = int(input("Enter SMTP port (usually 587): "))
        return smtp_server, port

def send_email(
    sender_email,
    password,
    to_emails,
    cc_emails,
    subject,
    body,
    attachment_paths
):
    smtp_server, port = get_smtp_settings(sender_email)

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(to_emails)
    message["Cc"] = ", ".join(cc_emails)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    for filepath in attachment_paths:
        try:
            with open(filepath, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filepath.split('/')[-1]}"
                )
                message.attach(part)
        except Exception as e:
            print(f"Failed to attach {filepath}: {e}")

    all_recipients = [email for email in to_emails + cc_emails if email]

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, all_recipients, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    sender_email = input("Enter your email address: ").strip()
    password = input("Enter your app password: ").strip()
    to_emails = [email.strip() for email in input("Enter recipient emails (comma-separated): ").split(",") if email.strip()]
    cc_emails = [email.strip() for email in input("Enter CC emails (comma-separated): ").split(",") if email.strip()]
    subject = input("Enter the subject: ").strip()
    print("Enter the body (end with a blank line):")
    body_lines = []
    while True:
        line = input()
        if line == "":
            break
        body_lines.append(line)
    body = "\n".join(body_lines)

    print("Choose files to attach (you can select multiple files):")
    attachment_paths = choose_files()

    send_email(
        sender_email,
        password,
        to_emails,
        cc_emails,
        subject,
        body,
        attachment_paths
    )
