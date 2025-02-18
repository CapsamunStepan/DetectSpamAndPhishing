import imaplib
import email
from email.header import decode_header


def decode_str(s):
    if not s:
        return None
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def check_OAuth2key(username_, password_):
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(username_, password_)
        mail.logout()
        return True
    except:
        return False


def get_total_messages_count(username_, password_):
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(username_, password_)
        mail.select('inbox')

        result, data = mail.select('inbox', readonly=True)
        total_messages = int(data[0])
        mail.logout()

        return total_messages
    except:
        return 0


def read_emails(username_, password_, messages_ids):
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(username_, password_)
    except:
        return {}, 0
    mail.select('inbox')

    messages = {}

    for email_id in messages_ids:
        result, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        from_ = decode_str(msg.get('From'))
        subject = decode_str(msg.get('Subject'))
        date = decode_str(msg.get('Date'))

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    part_body = part.get_payload(decode=True).decode()
                except:
                    continue
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part_body
        else:
            body = msg.get_payload(decode=True).decode()

        messages[email_id.decode()] = {
            'From': from_,
            'Subject': subject,
            'Date': date,
            'Body': body
        }

    mail.logout()

    return messages
