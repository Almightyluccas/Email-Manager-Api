import time
from fastapi import APIRouter, HTTPException, Body
from typing import Optional

from .models import LoginData
from ..utils.EmailInterface import EmailInterface
from ..utils.MailboxInterface import MailboxInterface
from ..utils.ImapExceptionCustom import ImapExceptionCust
from ..utils.config import imapURLDict

router = APIRouter()


@router.post("/emails/all/{mailbox}")
async def get_emails(
        mailbox: str,
        data: LoginData = Body(...),
        batch_size: Optional[int] = 5,
        number_of_emails: Optional[int] = 10):
    try:
        with EmailInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as email_client:
            start_time_fetching = time.time()
            fetched_emails = email_client.fetch_emails('ALL', batch_size, number_of_emails)
            fetching_time = time.time() - start_time_fetching
            return {
                'fetched': fetched_emails,
                "time_taken_fetching": fetching_time
            }
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post('/emails/all/before-date/{date}/{mailbox}')
async def get_emails_before_date(mailbox: str, date: str, data: LoginData = Body(...), flag: Optional[str] = None):
    try:
        with EmailInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as email_client:
            fetched_emails = email_client.fetchEmailBeforeDate(date, flag)
            return fetched_emails
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post('/emails/all/unseen/{mailbox}')
async def get_unseen_emails(mailbox: str, data: LoginData = Body(...), number_of_emails: Optional[int] = 10):
    try:
        with EmailInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as email_client:
            fetched_emails = email_client.fetch_emails('UNSEEN', number_of_emails)
            return fetched_emails
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post('/mailboxes/all')
async def get_all_mailboxes(data: LoginData = Body(...)):
    try:
        with MailboxInterface(data.email, data.password, imapURLDict[data.provider]) as mailbox_client:
            mailboxes = mailbox_client.fetchAllMailboxes()
            return mailboxes
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post('/mailboxes/count/{mailbox}')
async def get_total_emails_in_specific_mailbox(mailbox: str, data: LoginData = Body(...)):
    try:
        with MailboxInterface(data.email, data.password, imapURLDict[data.provider], mailbox) as mailbox_client:
            total_emails = mailbox_client.fetch_total_emails_in_current_mailbox()
            return total_emails
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post('/emails/mailboxes/{email_id}/transfer/{mailbox_from}/{mailbox_to}')
async def transfer_email(email_id: str, mailbox_from: str, mailbox_to: str, data: LoginData = Body(...)):
    return {'message': 'test transfer email route'}


@router.post('/mailboxes/create/{mailbox_name}')
async def create_mailbox(mailbox_name: str, data: LoginData = Body(...)):
    try:
        with MailboxInterface(data.email, data.password, imapURLDict[data.provider]) as mailbox_client:
            response = mailbox_client.create_new_mailbox(mailbox_name)
            return response
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete('/mailboxes/delete/{mailbox_name}')
async def delete_mailbox(mailbox_name: str, data: LoginData = Body(...)):
    try:
        with MailboxInterface(data.email, data.password, imapURLDict[data.provider], mailbox_name) as mailbox_client:
            response = mailbox_client.delete_mailbox(mailbox_name)
            return response
    except ImapExceptionCust as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete('/emails/trash/transfer/{email_id}')
async def transfer_email_to_trash(email_id: str, mailbox_from: str):
    return {'message': 'test transfer to trash'}


@router.delete('/emails/trash/delete')
async def empty_delete_folder(data: LoginData = Body(...), number_of_emails: Optional[int] = None):
    return {'message': 'test delete route'}
