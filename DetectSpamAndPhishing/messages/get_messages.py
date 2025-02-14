import imaplib
import email
from email.header import decode_header


def decode_str(s):
    """Декодирует строку из email-заголовка."""
    if not s:
        return None
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def read_emails(username_, password_, limit=15, offset=0):
    # Подключаемся к серверу Gmail
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username_, password_)
    mail.select('inbox')

    # Получаем идентификаторы писем (самые новые идут в конце)
    result, data = mail.search(None, 'ALL')
    ids = data[0].split()

    # Количество доступных писем
    total_messages = len(ids)

    # Определяем границы для пагинации
    start = max(0, total_messages - (offset + limit))
    end = max(0, total_messages - offset)

    # Отбираем нужные идентификаторы
    selected_ids = ids[start:end]

    messages = {}

    for email_id in reversed(selected_ids):  # Начинаем с самых новых
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

    return messages, total_messages
