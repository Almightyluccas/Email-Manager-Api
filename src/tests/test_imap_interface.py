from classes.imapInterface_Test import IMAPInterfaceTest as Imap
from classes.testUtils import TestUtilities
import time
import multiprocessing

test = TestUtilities()

information_needed = test.parse_json_file('/home/lamorim/PycharmProjects/Email-Manager-Api/private/request_body.json')
login_info = information_needed['login']['second']
imapURL = information_needed['imapURL']


def test_fetch_emails_wrapper(criteria: str, limit: int):
    email_client = Imap(login_info['email'], login_info['password'], imapURL['outlook'], 'inbox')
    email_client.test_fetch_emails_method(criteria, limit)
    email_client.closeConnection()


num_processes = 10

processes = []

for _ in range(num_processes):
    p = multiprocessing.Process(target=test_fetch_emails_wrapper, args=('ALL', 100))
    processes.append(p)
    p.start()

for p in processes:
    p.join()
