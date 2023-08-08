# FastAPI Email Fetching API
This repository contains a FastAPI-based RESTful API for fetching emails from various 
email providers using IMAP (Internet Message Access Protocol). It provides several endpoints to fetch emails, 
fetch mailbox details, and perform other email-related actions. Please make sure to check documentation for updates 
on project

**NOTE**: This project is still a work in progress and I plan on hosting the API in the cloud once all basic
endpoints have been implemented

## Usage

1. Start by visiting the API documentation page: [MailMasterPro API Docs](https://email-manager-restapi-staging-4cd12bf74fde.herokuapp.com/docs).

2. Choose the API route you intend to use and complete the required data fields.

3. After making the request, you'll receive a JSON payload containing the desired data.

***Note: For making requests to these routes, you can also use the fetch API or any HTTP client library of your choice.*** 

## Endpoints

The API provides the following endpoints:

### Fetch Emails

- **POST** `/emails/all/{mailbox}`
  Fetch emails from a specific mailbox.
  - Parameters:
    - `mailbox`: The name of the mailbox to fetch emails from.
    - `data`: JSON data containing `email`, `password`, and `provider` (email service provider) fields.
    - `number_of_emails`: (Optional) The maximum number of emails to fetch.

### Fetch Emails Before a Date

- **POST** `/emails/all/before-date/{date}/{mailbox}`
  Fetch emails from a specific mailbox before a given date.
  - Parameters:
    - `date`: The date in the format 'YYYY-MM-DD' to fetch emails before.
    - `mailbox`: The name of the mailbox to fetch emails from.
    - `data`: JSON data containing `email`, `password`, and `provider` fields.
    - `flag`: (Optional) A flag to filter emails (if applicable).

### Fetch Unseen Emails

- **POST** `/emails/all/unseen/{mailbox}`
  Fetch unseen emails from a specific mailbox.
  - Parameters:
    - `mailbox`: The name of the mailbox to fetch unseen emails from.
    - `data`: JSON data containing `email`, `password`, and `provider` fields.
    - `number_of_emails`: (Optional) The maximum number of unseen emails to fetch.

### Fetch All Mailboxes

- **POST** `/emails/mailboxes/all`
  Fetch all mailboxes for the given email account.
  - Parameters:
    - `data`: JSON data containing `email`, `password`, and `provider` fields.

### Fetch Total Number of Emails in a Mailbox

- **POST** `/emails/mailboxes/{mailbox}/count`
  Fetch the total number of emails in a specific mailbox.
  - Parameters:
    - `mailbox`: The name of the mailbox to get the email count for.
    - `data`: JSON data containing `email`, `password`, and `provider` fields.

### Transfer Email Between Mailboxes

- **POST** `/emails/mailboxes/{email_id}/transfer/{mailbox_from}/{mailbox_to}`
  Transfer an email from one mailbox to another.
  - Parameters:
    - `email_id`: The ID of the email to be transferred.
    - `mailbox_from`: The name of the source mailbox.
    - `mailbox_to`: The name of the destination mailbox.
    - `data`: JSON data containing `email`, `password`, and `provider` fields.

### Transfer Email to Trash

- **DELETE** `/emails/trash/transfer/{email_id}`
  Transfer an email to the trash folder.
  - Parameters:
    - `email_id`: The ID of the email to be transferred to the trash folder.
    - `mailbox_from`: The name of the source mailbox.

### Empty Delete Folder

- **DELETE** `/emails/trash/delete`
  Empty the delete folder (trash) of the email account.
  - Parameters:
    - `data`: JSON data containing `email`, `password`, and `provider` fields.
    - `number_of_emails`: (Optional) The maximum number of emails to delete from the trash.

For more details, consult the provided API documentation schemas for LoginData, ValidationError, and HTTPValidationError.
