from src.api.mailsender.mailer import Mailer

import imaplib
import email
import random
import time

import pytest

receiver_imap_server = "your.server.com"  # TODO: Change it
receiver_username = "youremailaddress@provider.com"
receiver_password = "yourpassword"
    

@pytest.mark.skip()  # TODO: This is test is NOT completed.
def test_send_email():
    """
    Check if mailer is able for sending emails.
    """
    mailer = Mailer()

    code = random.randint(10**6, 10**7)
    received = False

    target_subject = f"Unit Test - {int(time.time())}"
    target_content = f"This is a message sent from an unit testing.\n<h3>Code:<h3> {code}"

    mailer.send_message(
        dest_email=receiver_username,
        subject=target_subject,
        message=target_content
    )

    time.wait(5)  # Wait some time to check the inbox.

    client = imaplib.IMAP4_SSL(receiver_imap_server)
    client.login(receiver_username, receiver_password)

    status, n_messages = client.select("INBOX")
    n_first_messages = 3

    for index in range(n_messages, n_messages - n_first_messages, -1):

        res, message = client.fetch(str(index), "(RFC822)")

        for response in message:
            message = email.message_from_bytes(response[1])

            # Decode subject.
            subject, encoding = email.header.decode_header(message["Subject"])[0]

            if isinstance(subject, bytes):
                subject = subject.decode(encoding)
                    
            # Decode email sender.
            origin, encoding = email.header.decode_header(message.get("From"))[0]
                
            if isinstance(origin, bytes):
                origin = origin.decode(encoding)

            # Get the email body
            body = message.get_payload(decode=True).decode()
                
            # Caught the email.
            if target_content in body and subject == target_subject:
                received = True
                break
    
    assert received

