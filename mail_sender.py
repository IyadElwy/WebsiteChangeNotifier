import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:

    def __init__(self, mail: str, password: str):
        """
        Initializing the Mailing system object with the needed data.
        :param mail: your mail
        :type mail: str
        :param password: your mail password
        :type password: str
        """
        self._port = 465
        self._smtp_server_domain_name = "smtp.gmail.com"
        self._sender_mail = mail
        self._password = password
        self._html_msg = ""

    def _convert_to_sendable_html(self) -> str:
        msg_root = MIMEMultipart('related')
        msg_root['Subject'] = "Website Notifier"

        msg_alternative = MIMEMultipart('alternative')
        msg_root.attach(msg_alternative)

        msg_text = MIMEText(self._html_msg, 'html')
        msg_alternative.attach(msg_text)

        return msg_root.as_string()

    def send(self, email: str, subject: str, content: str, html_msg_to_send: str = ""):
        """
        The function to call when sending a mail
        :param email: the mail you wish to send to
        :type email: str
        :param subject: the subject of the mail
        :type subject: str
        :param content: The content of the mail
        :type content: str
        :param html_msg_to_send: the html message to send
        :type html_msg_to_send: str
        :return: None
        :rtype: None
        """
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self._smtp_server_domain_name, self._port,
                                   context=ssl_context)
        service.login(self._sender_mail, self._password)

        if html_msg_to_send:
            self._html_msg = html_msg_to_send
            service.sendmail(self._sender_mail, email,
                             self._convert_to_sendable_html())
        else:
            service.sendmail(self._sender_mail, email,
                             f"Subject: {subject}\n{content}")
        service.quit()
