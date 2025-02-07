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


def read_emails(username_, password_):
    # Подключаемся к серверу Gmail
    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    # Логинимся
    mail.login(username_, password_)

    # Выбираем ящик входящих писем
    mail.select('inbox')

    # Получаем идентификаторы всех писем
    result, data = mail.search(None, 'ALL')

    # data - строка, содержащая пробел-разделённые идентификаторы писем
    # Разбиваем строку на отдельные идентификаторы
    ids = data[0].split()

    # Словарь для хранения писем
    messages = {}

    # Читаем письма
    for email_id in ids:
        result, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Получаем информацию о письме
        from_ = decode_str(msg.get('From'))
        subject = decode_str(msg.get('Subject'))
        date = decode_str(msg.get('Date'))

        # Обработка тела письма
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                except Exception as e:
                    print(e)
                    pass
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    # Добавляем информацию о письме в словарь messages
                    messages[email_id] = {
                        'From': from_,
                        'Subject': subject,
                        'Date': date,
                        'Body': body
                    }
        else:
            content_type = msg.get_content_type()
            body = msg.get_payload(decode=True).decode()
            if content_type == "text/plain":
                # Добавляем информацию о письме в словарь messages
                messages[email_id] = {
                    'From': from_,
                    'Subject': subject,
                    'Date': date,
                    'Body': body
                }

    # Закрываем соединение
    mail.logout()

    return messages


if __name__ == '__main__':
    from user import password, username
    messages = read_emails(username, password)
    for message_id, message_data in messages.items():
        print(message_data['Body'])
