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
