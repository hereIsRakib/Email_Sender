import smtplib
from email.message import EmailMessage
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b'

mail_loc = input('Enter the mails.txt file location: ')
content_loc = input('Enter the Content.txt file location: ')
user_mail = input('Enter your Mail: ')
user_pass = input('Enter your mail passwords: ')

with open(mail_loc) as mail_file:
    mail = mail_file.read()
    print(mail)

with open(content_loc) as content_file:
    content = content_file.read()

all_mail_addresses = [item for item in mail.split('\n')]
print(all_mail_addresses)


def valid_mail(email):
    return re.fullmatch(regex, email)


mail_addresses = list(filter(valid_mail, all_mail_addresses))

email = EmailMessage()
email['to'] = ','.join(mail_addresses)
email['subject'] = input('Please Enter the Email Subject: ')
email.set_content(content)

attachments = input('Do you want to attach any files? (y/n): ')
if attachments.lower() == 'y':
    attachment_loc = input('Enter the attachment file location: ')
    with open(attachment_loc, 'rb') as attachment_file:
        attachment_data = attachment_file.read()
        attachment_name = input('Enter the attachment file name: ')
    email.add_attachment(attachment_data, maintype='application', subtype='octet-stream', filename=attachment_name)

with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(user_mail, user_pass)
    smtp.send_message(email)
    print(f'The mail has been sent to {", ".join(mail_addresses)}')
