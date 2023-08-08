from classes.imapInterface_Test import IMAPInterfaceTest as Imap
from classes.testUtils import TestUtilities
from src.utils.ImapInterface import ImapExceptionCust
import time

test = TestUtilities()

information_needed = test.parse_json_file('/home/lamorim/PycharmProjects/Email-Manager-Api/private/request_body.json')
login_info = information_needed['login']['second']
imapURL = information_needed['imapURL']

try:
    with Imap(login_info['email'], login_info['password'], imapURL['outlook'], 'inbox') as email_client:
        start_time_threads = time.time()
        result = email_client.fetch_emails('all', 10, 100)
        threaded_time = time.time() - start_time_threads
        print("Threaded time: %.2f seconds" % threaded_time)
        print(result['totalFetched'])

        # Check for duplicates
        email_ids = set()
        duplicate_count = 0
        for email in result['emails']:
            email_id = email['Message ID']
            if email_id in email_ids:
                print("Duplicate email:", email_id)
                duplicate_count += 1
            else:
                email_ids.add(email_id)

        print("Total duplicates:", duplicate_count)

except ImapExceptionCust as ce:
    print(ce.status_code, ce.detail)
