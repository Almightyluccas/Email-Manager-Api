from .ImapInterface import IMAPInterface
from .ImapExceptionCustom import ImapExceptionCust
from typing import Dict, List


class MailboxInterface(IMAPInterface):
    def fetchAllMailboxes(self) -> Dict[str, List[bytes]]:
        try:
            response = self.mail.list()
            _, mailboxes_data = response
            mailboxes = [mailbox.decode().split()[-1].strip('"') for mailbox in mailboxes_data]
            return {'mailboxes': mailboxes}
        except Exception as e:
            ImapExceptionCust(500, str(e))

    def fetch_total_emails_in_current_mailbox(self) -> Dict[str, int]:
        try:
            status, response = self.mailbox
            self.mail.close()

            if status == 'OK':
                total_emails_num = int(response[0])
                return {'totalEmailsNum': total_emails_num}
        except Exception as e:
            ImapExceptionCust(500, str(e))

    def create_new_mailbox(self, mailbox_name: str):
        try:
            status, response = self.mail.create(mailbox_name)
            if status != 'OK':
                message = f"Failed to create mailbox: {response}"
                raise ImapExceptionCust(500, message)
            return {'status_code': 200, 'message': f"Mailbox '{mailbox_name}' created successfully"}
        except Exception as e:
            raise ImapExceptionCust(500, str(e))

    def delete_mailbox(self, mailbox_name: str):
        try:
            status, email_ids = self.mail.search(None, 'ALL')
            email_id_list = email_ids[0].split()

            if len(email_id_list) > 0:
                message = "Failed to delete mailbox. Make sure Mailbox is empty before deleting mailbox"
                raise ImapExceptionCust(500, message)

            response, message = self.mail.delete(mailbox_name)
            if response != 'OK':
                raise ImapExceptionCust(500, message)
            return {'status_code': 200, 'message': f"Mailbox '{mailbox_name}' was successfully deleted"}
        except Exception as e:
            raise ImapExceptionCust(500, str(e))
