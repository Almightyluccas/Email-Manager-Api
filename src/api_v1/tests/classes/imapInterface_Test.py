from src.utils.MailboxInterface import MailboxInterface
from src.utils.EmailInterface import EmailInterface
from typing import List, Dict, Union, Any
from src.utils.ImapExceptionCustom import ImapExceptionCust
import email
import time


class IMAPInterfaceTest(MailboxInterface, EmailInterface):

    def test_fetch_total_emails_in_current_mailbox(self):
        print("Executing fetchAllMailboxes()...")
        start_time_fetch_fetchAllMailboxes = time.time()
        self.fetch_total_emails_in_current_mailbox()
        print("--- %s seconds ---\n" % (time.time() - start_time_fetch_fetchAllMailboxes))

    def test_fetchAllMailboxes_method(self):
        print("Executing fetchAllMailboxes()...")
        start_time_fetch_fetchAllMailboxes = time.time()
        self.fetchAllMailboxes()
        print("--- %s seconds ---\n" % (time.time() - start_time_fetch_fetchAllMailboxes))

    def test_fetchEmailBeforeDate(self, date: str, flag: str = None):
        start_time_fetch_before_date = time.time()
        print(self.fetchEmailBeforeDate(date, flag))
        print("--- %s seconds ---\n" % (time.time() - start_time_fetch_before_date))

    def test_fetch_emails_method(self, criteria: str, limit: int):
        print("Executing fetch_emails()...")
        self.fetch_emails(criteria, limit)

