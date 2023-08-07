import queue
import time

from fastapi import FastAPI, HTTPException, Body
from typing import Optional
from pydantic import BaseModel
from classes.EmailInterface import EmailInterface
from classes.MailboxInterface import MailboxInterface
from classes.ImapExceptionCustom import ImapExceptionCust
import threading

app = FastAPI(debug=True)

imapURLDict = {
    'gmail': 'imap.gmail.com',
    'outlook': 'outlook.office365.com',
    'yahoo': 'imap.mail.yahoo.com',
    'aol': 'imap.aol.com'
}

emails = {'emails': None,
          'totalFetched': 0
          }
emails_lock = threading.Lock()

def test_fetch_emails_wrapper(criteria: str, batch_size: int, total_emails: int, data):
    try:
        with EmailInterface(data.email, data.password, imapURLDict[data.provider], 'inbox') as email_interface:
            fetched_emails = email_interface.fetch_emails(criteria, batch_size, total_emails)

            # Acquire the lock before updating the list and counter
            with emails_lock:
                if emails['emails'] is None:
                    emails['emails'] = []
                emails['emails'] += (fetched_emails['emails'])
                emails['totalFetched'] += fetched_emails['totalFetched']
    except ImapExceptionCust as ce:
        return ce.status_code, ce.detail




class LoginData(BaseModel):
    email: str
    password: str
    provider: str


@app.post("/emails/all/{mailbox}")
async def get_emails(mailbox: str, data: LoginData = Body(...), number_of_emails: Optional[int] = 10):
    try:
        with EmailInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as email_client:
            start_time_threads = time.time()
            emails = email_client.fetch_emails('ALL', 10, number_of_emails)
            threaded_time = time.time() - start_time_threads
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return {
        "emails": emails['emails'],
        "total_fetched": emails['totalFetched'],
        "threaded_time": threaded_time
    }


@app.post('/emails/all/before-date/{date}/{mailbox}')
async def get_emails_before_date(mailbox: str, date: str, data: LoginData = Body(...), flag: Optional[str] = None):
    try:
        with EmailInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as email_client:
            emails = email_client.fetchEmailBeforeDate(date, flag)
            return emails
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.post('/emails/all/unseen/{mailbox}')
async def get_unseen_emails(mailbox: str, data: LoginData = Body(...), number_of_emails: Optional[int] = 10):
    try:
        with EmailInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as email_client:
            emails = email_client.fetch_emails('UNSEEN', number_of_emails)
            return emails
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.post('/mailboxes/all')
async def get_all_mailboxes(data: LoginData = Body(...)):
    try:
        with MailboxInterface(data.email, data.password, imapURLDict[data.provider]) as mailbox_client:
            mailboxes = mailbox_client.fetchAllMailboxes()
            return mailboxes
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.post('/mailboxes/count/{mailbox}')
async def get_total_emails_in_specific_mailbox(mailbox: str, data: LoginData = Body(...)):
    try:
        with MailboxInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as mailbox_client:
            total_emails = mailbox_client.fetch_total_emails_in_current_mailbox()
            return total_emails
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.post('/emails/mailboxes/{email_id}/transfer/{mailbox_from}/{mailbox_to}')
async def transfer_email(email_id: str, mailbox_from: str, mailbox_to: str, data: LoginData = Body(...)):
    return {'message': 'test transfer email route'}


@app.post('/mailboxes/create/{mailbox_name}')
async def create_mailbox(mailbox_name: str, data: LoginData = Body(...)):

    return {'message': 'test create mailbox route'}


@app.delete('/mailboxes/delete/{mailbox_name')
async def delete_mailbox(mailbox_name: str, data: LoginData = Body(...)):
    # make sure that only user created mailboxes can be deleted,
    # meaning that default mailboxes must remain (list of defaults)
    return {'message': 'test mailbox delete route'}


@app.delete('/emails/trash/transfer/{email_id}')
async def transfer_email_to_trash(email_id: str, mailbox_from: str):
    return {'message': 'test transfer to trash'}


@app.delete('/emails/trash/delete')
async def empty_delete_folder(data: LoginData = Body(...), number_of_emails: Optional[int] = None):
    return {'message': 'test delete route'}


@app.post("/test")
async def test_new_route(criteria: str, batch_size: int, total_emails: int, data: LoginData):
    start_time_threads = time.time()

    print('\nThreading...')
    num_threads = 5
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(
            target=test_fetch_emails_wrapper,
            args=(criteria, batch_size, num_threads * 10, data))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    threaded_time = time.time() - start_time_threads

    return {
        "emails": emails['emails'],
        "total_fetched": emails['totalFetched'],
        "threaded_time": threaded_time
    }











