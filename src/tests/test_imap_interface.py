from classes.imapInterface_Test import IMAPInterfaceTest as Imap
from classes.testUtils import TestUtilities
from src.classes.ImapInterface import ImapExceptionCust
import time
import multiprocessing

# def test_fetch_emails_wrapper(criteria: str, limit: int):
#     email_client = Imap(login_info['email'], login_info['password'], imapURL['outlook'], 'inbox')
#     email_client.test_fetch_emails_method(criteria, limit)
#     email_client.closeConnection()

test = TestUtilities()

information_needed = test.parse_json_file('/home/lamorim/PycharmProjects/Email-Manager-Api/private/request_body.json')
login_info = information_needed['login']['main']
imapURL = information_needed['imapURL']
email_client = Imap(login_info['email'], login_info['password'], imapURL['outlook'], 'inbox')

try:
    with Imap(login_info['email'], '343434WFD', imapURL['outlook'], 'inbox') as email_client:
        print(email_client.fetchTotalNumberEmails())
except ImapExceptionCust as ce:
    print(ce.status_code, ce.detail)

#
#
# num_processes = 10
#
# processes = []
#
# for _ in range(num_processes):
#     p = multiprocessing.Process(target=test_fetch_emails_wrapper, args=('ALL', 100))
#     processes.append(p)
#     p.start()
#
# for p in processes:
#     p.join()
