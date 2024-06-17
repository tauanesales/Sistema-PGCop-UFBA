__all__ = ["localmail", "Mail"]


class Mail(object):
    def __init__(self, origin_email, subject, content):
        self.origin = origin_email
        self.subject = subject
        self.content = content

    def __str__(self) -> str:
        return f"<Mail: {self.origin} | {self.subject}>"


class LocalMail(object):
    """
    Class for simulating a mail locally.
    """

    def __init__(self):
        self.__accounts = dict()

    def send(self, from_email, dest_email: str, subject: str, html_content: str):
        """
        Send a mail.
        """
        if dest_email not in self.__accounts:
            self.__accounts[dest_email] = list()

        inbox = self.__accounts[dest_email]
        inbox.append(Mail(from_email, subject, html_content))

    def get_message(self, email, index=-1) -> Mail:
        """
        Get a mail.
        """
        if email not in self.__accounts:
            return None

        return self.__accounts[email][index]


localmail = LocalMail()
