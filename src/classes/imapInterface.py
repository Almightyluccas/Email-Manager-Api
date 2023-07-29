import email
import imaplib
from typing import Dict, Union, List, Tuple
from datetime import datetime


# noinspection PyUnresolvedReferences,PyTypeChecker
class IMAPInterface:

    def __init__(self, username: str, password: str, imapURL: str, mailbox: str = None) -> None:
        self.mail = imaplib.IMAP4_SSL(imapURL)
        self.mail.login(username, password)
        if mailbox is not None:
            self.mailbox = self.mail.select(mailbox)

    def fetchAllEmails(self, limit: int = None) -> Union[Dict[str, str], Dict[str, List[Dict[str, str]]]]:
        try:
            if not self.mail:
                raise ValueError("Not connected to the mail server. Call 'connect()' first.")

            _, data = self.mail.search(None, 'ALL')
            email_ids = data[0].split()

            if limit is not None:
                start = max(0, len(email_ids) - limit)
                email_ids = email_ids[start:]
            emails = []
            for total_fetched, email_id in enumerate(email_ids):
                _, msg_data = self.mail.fetch(email_id, '(BODY.PEEK[])')
                msg = email.message_from_bytes(msg_data[0][1])
                emails.append({
                    'From': msg['From'],
                    'To': msg['To'],
                    'Subject': msg['Subject'],
                    'Date': msg['Date'],
                    'Message ID': msg['Message-ID'],
                    'Message Body': msg.as_string(),
                })
                self.mail.store(email_id, '-FLAGS', '\\Seen')  # adds around 1 ms response time
            return {
                'emails': emails,
                'totalFetched': total_fetched + 1
            }
        except Exception as e:
            return {'error': str(e)}

    def fetchEmailBeforeDate(self, fetchBeforeDate: str) -> Union[Dict[str, str], Dict[str, List[Dict[str, str]]]]:
        result, data = self.mail.uid('search', None, f'(BEFORE "{fetchBeforeDate}")')
        fetched_email = []

        if result == 'OK':
            emailIdList = data[0].split()
            for total_fetched, num in enumerate(emailIdList):
                result, emailData = self.mail.uid('fetch', num, '(BODY.PEEK[HEADER])')
                if result == 'OK':
                    if emailData[0] is not None and emailData[0][1] is not None:
                        rawEmail = emailData[0][1].decode("utf-8", errors='ignore')
                        emailMessage = email.message_from_string(rawEmail)
                        dataTuple = email.utils.parsedate_tz(emailMessage['Date'])

                        if dataTuple:
                            localDate = datetime.fromtimestamp(email.utils.mktime_tz(dataTuple))
                            subject = emailMessage['Subject']
                            senderName, senderEmail = email.utils.parseaddr(emailMessage['From'])

                            fetched_email.append({
                                'Date': localDate,
                                'Sender Name': senderName,
                                'Sender Email': senderEmail,
                                'Subject': subject,
                                'UID': num
                            })
                    else:
                        print("No email data for UID ", num)
        self.mail.close()
        return {
            'emails': fetched_email,
            'totalFetched': total_fetched + 1
        }

    def fetchAllMailboxes(self) -> Dict[str, List[bytes]]:
        response = self.mail.list()
        _, mailboxes_data = response
        mailboxes = [mailbox.decode().split()[-1].strip('"') for mailbox in mailboxes_data]
        return {'mailboxes': mailboxes}

    def fetchTotalNumberEmails(self) -> Dict[str, int]:
        status, response = self.mailbox
        self.mail.close()

        if status == 'OK':
            total_emails_num = int(response[0])
            return {'totalEmailsNum': total_emails_num}

    def deleteMarkedEmails(self, deleteBeforeDate: str) -> Tuple[int, List[str]]:
        markedEmails = self.fetchEmailBeforeDate(deleteBeforeDate)
        successfullyDeleted = 0
        errors = []

        for mail in markedEmails:
            try:
                self.mail.uid('store', mail['UID'], '+FLAGS', '\\Deleted')
                successfullyDeleted += 1
            except Exception as e:
                errors.append(f"Error deleting email with UID {mail['UID']}: {str(e)}")
        try:
            self.mail.expunge()
            return successfullyDeleted, errors
        except Exception as e:
            return 0, [f"Error occurred during expunge: {str(e)}"]

    def closeConnection(self) -> None:
        self.mail.logout()
