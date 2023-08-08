import email
from typing import Dict, Union, List, Tuple, Any
from datetime import datetime
from .ImapInterface import IMAPInterface
from .ImapExceptionCustom import ImapExceptionCust


class EmailInterface(IMAPInterface):
    def __init__(self, username: str, password: str, imapURL: str, mailbox: str = None):
        super().__init__(username, password, imapURL, mailbox)
        self.fetched_email_ids = set()

    def clear_fetched_email_ids(self):
        self.fetched_email_ids.clear()

    def fetch_emails(self, criteria: str, batch_size: int, total_emails: int) \
            -> dict[str, list[dict[str, str | Any]] | int]:
        try:
            _, data = self.mail.search(None, criteria)
            email_ids = data[0].split()

            new_email_ids = [email_id for email_id in email_ids if email_id not in self.fetched_email_ids]
            num_batches = (total_emails + batch_size - 1) // batch_size

            emails = []
            total_fetched = 0

            for page in range(1, num_batches + 1):
                start = (page - 1) * batch_size
                end = min(page * batch_size, len(new_email_ids))
                batch_ids = new_email_ids[start:end]
                batch_emails = []

                for email_id in batch_ids:
                    _, msg_data = self.mail.fetch(email_id, '(BODY.PEEK[])')
                    msg = email.message_from_bytes(msg_data[0][1])
                    batch_emails.append({
                        'From': msg['From'],
                        'To': msg['To'],
                        'Subject': msg['Subject'],
                        'Date': msg['Date'],
                        'Message ID': msg['Message-ID'],
                        'Message Body': msg.as_string(),
                    })
                    self.fetched_email_ids.add(email_id)
                    total_fetched += 1

                emails.extend(batch_emails)

            return {'emails': emails, 'totalFetched': total_fetched}
        except Exception as e:
            raise ImapExceptionCust(500, str(e))

    def fetchEmailBeforeDate(self, fetchBeforeDate: str, optional_flag: str = None) \
            -> Union[Dict[str, str], Dict[str, List[Dict[str, str]]]]:
        try:
            result, data = self.mail.uid('search', None, f'(BEFORE "{fetchBeforeDate}")')
            fetched_email = []
            total_fetched = 0

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
                                if optional_flag:
                                    flag_to_set = f'({optional_flag})'
                                    self.mail.uid('store', num, '+FLAGS', flag_to_set)
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
            return {'emails': fetched_email, 'totalFetched': total_fetched + 1}
        except Exception as e:
            raise ImapExceptionCust(500, str(e))

    def deleteMarkedEmails(self, deleteBeforeDate: str) -> Tuple[int, List[str]]:
        try:
            markedEmails = self.fetchEmailBeforeDate(deleteBeforeDate)
            successfullyDeleted = 0
            errors = []

            for mail in markedEmails:
                try:
                    # noinspection PyTypeChecker
                    self.mail.uid('store', mail['UID'], '+FLAGS', '\\Deleted')
                    successfullyDeleted += 1
                except Exception as e:
                    ImapExceptionCust(500, str(e))
                self.mail.expunge()
                return successfullyDeleted, errors
        except Exception as e:
            ImapExceptionCust(500, str(e))