

## Potential Performance Hits

```python
      for email_id in email_ids:
                _, msg_data = self.mail.fetch(email_id, '(BODY.PEEK[])')
                msg = email.message_from_bytes(msg_data[0][1])
                emails.append({
                    'From': msg['From'],
                    'To': msg['To'],
                    'Subject': msg['Subject'],
                    'Date': msg['Date'],
                    'Message ID': msg['Message-ID'],
                    'Message Body': msg.as_string(),
                })
                self.mail.store(email_id, '-FLAGS', '\\Seen')
 ```
* **Found**: `imapInterface.py` in the `fetchAllEmails(limit)` method within the for loop:
* **Hypothesis**: No tests have been done yet but this is for sure causing slower response time
* **Possible Solutions**: Possibly implement other data structure to check if performance increases




## Known Performance Hits
```python 
self.mail.store(email_id, '-FLAGS', '\\Seen') 
```
* **Found**: `imapInterface.py` in the `fetchAllEmails(limit)` method within the for loop:
  ```python
      for email_id in email_ids:
                _, msg_data = self.mail.fetch(email_id, '(BODY.PEEK[])')
                msg = email.message_from_bytes(msg_data[0][1])
                emails.append({
                    'From': msg['From'],
                    'To': msg['To'],
                    'Subject': msg['Subject'],
                    'Date': msg['Date'],
                    'Message ID': msg['Message-ID'],
                    'Message Body': msg.as_string(),
                })
                self.mail.store(email_id, '-FLAGS', '\\Seen')
  ```
* **Impact**: after minimal testing calling the API, with marking the items as seen would add
around `1.4s` in the response time when fetching `20 emails` with an avg time of `3.69s`
when removing the call to `mark as seen` the avg time was down to `2.30s`

* **Possible Solutions**:
  * optimize the request made to imap server so we don't need to mark as seen

## Future Version - Tests

### API Version 2:

#### &nbsp; Differnent email parsers to test:
* Currently using `email.parser` 

* `cemail` (cython-based email parsing) library instead of `email.parser` from the standard library
  * cemail is a Cython-based library that aims to provide faster email parsing. It is a drop-in replacement
  for Python's email.parser and claims to be significantly faster. Install it using:
    ```bash
    pip install cemail
    ```
*  `pymailparser` a library specifically designed for parsing emails. It claims to have better performance than 
Python's built-in email parsing libraries.
    * Install it using:
      ```bash
      pip install pymailparser
      ```
    
  