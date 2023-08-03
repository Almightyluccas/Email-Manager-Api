from fastapi import FastAPI, HTTPException, Body
from typing import Optional
from pydantic import BaseModel
from classes.imapInterface import IMAPInterface
from classes.imapInterface import ImapExceptionCust

app = FastAPI(debug=True)

imapURLDict = {
    'gmail': 'imap.gmail.com',
    'outlook': 'outlook.office365.com',
    'yahoo': 'imap.mail.yahoo.com',
    'aol': 'imap.aol.com'
}


class LoginData(BaseModel):
    email: str
    password: str
    provider: str


@app.post("/emails/all/{mailbox}")
async def get_emails(mailbox: str, data: LoginData = Body(...), number_of_emails: Optional[int] = 10):
    try:
        with IMAPInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as email_client:
            emails = email_client.fetch_emails('ALL', number_of_emails)
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return emails


@app.post('/emails/all/before-date/{date}/{mailbox}')
async def get_emails_before_date(mailbox: str, date: str, data: LoginData = Body(...), flag: Optional[str] = None):
    try:
        with IMAPInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as email_client:
            emails = email_client.fetchEmailBeforeDate(date, flag)
            return emails
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.post('/emails/all/unseen/{mailbox}')
async def get_unseen_emails(mailbox: str, data: LoginData = Body(...), number_of_emails: Optional[int] = 10):
    try:
        with IMAPInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as email_client:
            emails = email_client.fetch_emails('UNSEEN', number_of_emails)
            return emails
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.post('/emails/mailboxes/all')
async def get_all_mailboxes(data: LoginData = Body(...)):
    try:
        with IMAPInterface(data.email, data.password, imapURLDict[data.provider]) as email_client:
            mailboxes = email_client.fetchAllMailboxes()
            return mailboxes
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.post('/emails/mailboxes/{mailbox}/count')
async def get_total_number_of_emails(mailbox: str, data: LoginData = Body(...)):
    try:
        with IMAPInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as email_client:
            total_emails = email_client.fetchTotalNumberEmails()
            return total_emails
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.post('/emails/mailboxes/{email_id}/transfer/{mailbox_from}/{mailbox_to}')
async def transfer_email(email_id: str, mailbox_from: str, mailbox_to: str, data: LoginData = Body(...)):
    return {'message': 'test transfer email route'}


@app.post('/mailbox/create/{mailbox_name}')
async def create_mailbox(mailbox_name: str, data: LoginData = Body(...)):

    return {'message': 'test create mailbox route'}


@app.delete('/mailbox/delete/{mailbox_name')
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
