from classes.imapInterface_Test import IMAPInterfaceTest as Imap
from classes.testUtils import TestUtilities

test = TestUtilities()

information_needed = test.parse_json_file('/home/lamorim/PycharmProjects/Email-Manager-Api/private/request_body.json')
login_info = information_needed['login']['main']
imapURL = information_needed['imapURL']

email_client = Imap(login_info['email'], login_info['password'], imapURL['outlook'], 'inbox')
# test new methods below

print(email_client.fetchAllMailboxes())


email_client.closeConnection()

