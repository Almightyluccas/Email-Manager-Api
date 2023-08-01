from fastapi import FastAPI, HTTPException, Body
from typing import Optional
from pydantic import BaseModel
from classes.imapInterface import IMAPInterface

app = FastAPI(debug=True)

imapURLDict = {
    'gmail': 'imap.gmail.com',
    'outlook': 'imap-mail.outlook.com',
    'yahoo': 'imap.mail.yahoo.com',
    'aol': 'imap.aol.com'
}


class LoginData(BaseModel):
    email: str
    password: str
    provider: str


@app.post("/emails/all/{mailbox}")
async def get_emails(
        mailbox: str,
        data: LoginData = Body(...),
        number_of_emails: Optional[int] = None
):
    try:
        email_client = IMAPInterface(data.email, data.password, imapURLDict[data.provider], mailbox)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to login:  {e}")
    try:
        emails = email_client.fetch_emails('ALL', number_of_emails)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch emails")
    email_client.closeConnection()
    return emails


@app.post('/emails/all/before-date/{date}/{mailbox}')
async def get_emails_before_date(mailbox: str, date: str, data: LoginData = Body(...), flag: Optional[str] = None):
    try:
        email_client = IMAPInterface(data.email, data.password, imapURLDict[data.provider], mailbox)
    except Exception:
        raise HTTPException(status_code=400, detail='Failed to login')
    try:
            emails = email_client.fetchEmailBeforeDate(date, flag)
    except Exception:
        raise HTTPException(status_code=500, detail='Failed to fetch emails')
    email_client.closeConnection()
    return emails


@app.post('/emails/all/unseen/{mailbox}')
async def get_unseen_emails(mailbox: str, data: LoginData = Body(...), number_of_emails: Optional[int] = None):
    try:
        email_client = IMAPInterface(data.email, data.password, imapURLDict[data.provider], mailbox)
    except Exception:
        raise HTTPException(status_code=400, detail='Failed to login')
    try:
        email_client.fetch_emails('UNSEEN', number_of_emails)
    except Exception:
        raise HTTPException(status_code=500, detail='Failed to fetch mailboxes')


@app.post('/emails/mailboxes/all')
async def get_all_mailboxes(data: LoginData = Body(...)):
    try:
        email_client = IMAPInterface(data.email, data.password, imapURLDict[data.provider])
    except Exception:
        raise HTTPException(status_code=400, detail='Failed to login')
    try:
        mailboxes = email_client.fetchAllMailboxes()
    except Exception:
        raise HTTPException(status_code=500, detail='Failed to fetch mailboxes')
    email_client.closeConnection()
    return mailboxes


@app.post('/emails/mailboxes/{mailbox}/count')
async def get_total_number_of_emails(mailbox: str, data: LoginData = Body(...)):
    try:
        email_client = IMAPInterface(data.email, data.password, imapURLDict[data.provider], mailbox)
    except Exception:
        raise HTTPException(status_code=400, detail='Failed to login')
    try:
        total_emails = email_client.fetchTotalNumberEmails()
    except Exception:
        raise HTTPException(status_code=500, detail='Failed to fetch total number of emails')
    email_client.closeConnection()
    return total_emails


@app.post('/emails/mailboxes/{email_id}/transfer/{mailbox_from}/{mailbox_to}')
async def transfer_email(email_id: str, mailbox_from: str, mailbox_to: str, data: LoginData = Body(...)):
    return {'message': 'test transfer email route'}


@app.delete('emails/trash/transfer/{email_id}')
async def transfer_email_to_trash(email_id: str, mailbox_from: str):
    return {'message': 'test transfer to trash'}


@app.delete('/emails/trash/delete')
async def empty_delete_folder(data: LoginData = Body(...), number_of_emails: Optional[int] = None):
    return {'message': 'test delete route'}
