from src.classes.imapInterface import IMAPInterface
import time


class IMAPInterfaceTest(IMAPInterface):

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
        start_time_fetch_fetchAllMailboxes = time.time()
        self.fetch_emails(criteria, limit)
        print("--- %s seconds ---\n" % (time.time() - start_time_fetch_fetchAllMailboxes))

