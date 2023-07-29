from fastapi import FastAPI, Path, Query, HTTPException, status
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


@app.post("/email/all/{mailbox}")
async def get_emails(data: LoginData, mailbox: str, number_of_emails: Optional[int] = None):
    try:
        email_client = IMAPInterface(data.email, data.password, imapURLDict[data.provider], mailbox)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to login")
    try:
        emails = email_client.fetchAllEmails(number_of_emails)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch emails")
    email_client.closeConnection()
    return emails


@app.post('/email/all/before-date/{mailbox}/{date}')
async def get_emails_before_date(data: LoginData, mailbox: str, date: str):
    try:
        email_client = IMAPInterface(data.email, data.password, imapURLDict[data.provider], mailbox)
    except Exception:
        raise HTTPException(status_code=400, detail='Failed to login')
    try:
        emails = email_client.fetchEmailBeforeDate(date)
    except Exception:
        raise HTTPException(status_code=500, detail='Failed to fetch emails')
    email_client.closeConnection()
    return emails


@app.post('/email/all/unseen/{mailbox}')
async def get_unseen_emails(data: LoginData, mailbox: str):
    try:
        email_client = IMAPInterface(data.email, data.password, imapURLDict[data.provider], mailbox)
    except Exception:
        raise HTTPException(status_code=400, detail='Failed to login')
    try:
        email_client.fetchUnseenEmails()
    except:
        raise HTTPException(status_code=500, detail='Failed to fetch mailboxes')


@app.post('/email/get-all-mailboxes')
async def get_all_mailboxes(data: LoginData):
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


@app.post('/email/count/{mailbox}')
async def get_total_number_of_emails(data: LoginData, mailbox: str):
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
