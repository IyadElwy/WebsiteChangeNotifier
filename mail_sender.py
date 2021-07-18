import smtplib, ssl


class Mail:

    def __init__(self, mail, password):
        self._port = 465
        self._smtp_server_domain_name = "smtp.gmail.com"
        self._sender_mail = mail
        self._password = password

    def send(self, email, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self._smtp_server_domain_name, self._port,
                                   context=ssl_context)
        service.login(self._sender_mail, self._password)

        result = service.sendmail(self._sender_mail, email,
                                  f"Subject: {subject}\n{content}")

        service.quit()
