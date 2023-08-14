from classes.imapInterface_Test import IMAPInterfaceTest as Imap
from classes.testUtils import TestUtilities
from src.utils.ImapInterface import ImapExceptionCust
import threading
import multiprocessing
import time

test = TestUtilities()

information_needed = test.parse_json_file('/home/lamorim/PycharmProjects/Email-Manager-Api/private/request_body.json')
login_info = information_needed['login']['main']
imapURL = information_needed['imapURL']
email_client = Imap(login_info['email'], login_info['password'], imapURL['outlook'], 'inbox')

emails = {'emails': None, 'totalFetched': 0}


def test_fetch_emails_wrapper(criteria: str, batch_size: int, total_emails: int):
    try:
        with Imap(login_info['email'], login_info['password'], imapURL['outlook'], 'inbox') as email_interface:
            start_time = time.time()
            fetched_emails = email_interface.fetch_emails(criteria, batch_size, total_emails)
            with threading.Lock():
                if emails['emails'] is None:
                    emails['emails'] = []
                emails['emails'] += fetched_emails['emails']
                emails['totalFetched'] += fetched_emails['totalFetched']
            function_time = time.time() - start_time
            print("\nIndividual Function call time: %.2f seconds" % function_time)
            print(f"\nEmails Fetched: {fetched_emails['totalFetched']}")

    except ImapExceptionCust as ce:
        print(ce.status_code, ce.detail)


start_time_threads = time.time()

print('\nThreading...')
num_threads = 5
threads = []

for _ in range(num_threads):
    thread = threading.Thread(target=test_fetch_emails_wrapper, args=('ALL', 10, 100))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

threaded_time = time.time() - start_time_threads
print(emails)

print('\n\n' + 8 * '*' + ' Time Results ' + 8 * '*')
print("\nThreaded time: %.2f seconds" % threaded_time)
print(f"\nEmails Fetched: {emails['totalFetched']}")
