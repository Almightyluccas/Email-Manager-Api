# Tests
This is where documentation about test I have performed while creating the email
restAPI
### Email Server Test

#### Purpose: 
- Test theory to figure out if there is a difference between using a different
imap server url for outlook.
#### How: 
- Used Multiprocessing to run the testing locally
  ```python
  def test_fetch_emails_wrapper(criteria: str, limit: int):
    email_client = Imap(login_info['email'], login_info['password'], imapURL['outlook'], 'inbox')
    email_client.test_fetch_emails_method(criteria, limit)
    email_client.closeConnection()


  num_processes = 10

  processes = []

  for _ in range(num_processes):
    p = multiprocessing.Process(target=test_fetch_emails_wrapper, args=('ALL', 100))
    processes.append(p)
    p.start()

  for p in processes:
    p.join()
  ```

#### Results:
- outlook.office365.com 
  - **Average-** `12.74519992615448 seconds`
    - --- 15.561833143234253 seconds ---
    - --- 14.707858562469482 seconds ---
    - --- 11.736665725708008 seconds ---
    - --- 12.935247421264648 seconds ---
    - --- 11.706063747406006 seconds ---
    - --- 10.979416847229004 seconds ---
    - --- 11.475932359695435 seconds ---
    - --- 15.225568771362305 seconds ---
    - --- 11.666008949279785 seconds ---
    - --- 11.955414533615112 seconds ---

- imap-mail.outlook.com
  - **Average-** `12.315498707158127 seconds`
    - --- 11.592897891998291 seconds ---
    - --- 13.325559377670288 seconds ---
    - --- 11.608863830566406 seconds ---
    - --- 11.68841004371643 seconds --- 
    - --- 12.020949602127075 seconds ---  
    - --- 13.19546389579773 seconds --- 
    - --- 13.376948595046997 seconds ---
    - --- 11.579460859298706 seconds --- 
    - --- 11.97146201133728 seconds ---
    - --- 12.394320964813232 seconds ---

#### After Thought
- There are a couple of issues surrounding the test, some of these include:
  - Test was ran locally meaning that it won't fully take into account the API
environment where this will actually be deployed on
  - Upon running the test I came to realize that the response time also varies 
depending on when you make a request. Meaning sometimes it could be faster or slower, 
this is most likely due to high or low request on the imap server
- Now with taking the above into account, the time difference between imap
server address are negligible