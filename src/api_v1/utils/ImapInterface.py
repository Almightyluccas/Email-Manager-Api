import imaplib
from .ImapExceptionCustom import ImapExceptionCust


class IMAPInterface:
    def __enter__(self):
        print('user has connected to your server...') # todo: implement logging
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            raise ImapExceptionCust(500, f"An exception of type {exc_type} occurred: {exc_value}")
        print('user has exited from your server...')  # todo: implement logging
        self.mail.logout()

    def __init__(self, username: str, password: str, imapURL: str, mailbox: str = None) -> None:
        try:
            self.mail = imaplib.IMAP4_SSL(imapURL)
            self.mail.login(username, password)
            if mailbox is not None:
                self.mailbox = self.mail.select(mailbox)
                response_code, response_msg = self.mailbox
                if response_code != 'OK':
                    raise ImapExceptionCust(422, f"Mailbox '{mailbox}' does not exist.")
        except Exception as e:
            raise ImapExceptionCust(400, str(e))
