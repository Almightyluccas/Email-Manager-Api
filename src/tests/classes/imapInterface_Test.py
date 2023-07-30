from src.classes.imapInterface import IMAPInterface


class IMAPInterfaceTest(IMAPInterface):

    def test_fetchAllMailboxes_method(self):
        mailboxes = self.fetchAllMailboxes()
        return mailboxes

