# Working Routes

* [x] Get Emails
    ```python
    @app.post("/email/all/{mailbox}")
    ```
* [X] Get Emails Before Date
    ```python
    @app.post('/email/all/before-date/{mailbox}/{date}')
    ```
* [ ] Get Unseen Emails
    ```python
    @app.post('/email/all/unseen/{mailbox}')
    ```
* [X] Get All Mailboxes
    ```python
    @app.post('/email/mailboxes')
    ```
* [X] Get Total Number Of emails
    ```python
    @app.post('/email/count/{mailbox}')
    ```

