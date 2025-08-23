import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.application.usecases.tickets.email import EmailSenderInterface
from src.infrastructure.email_sender.config import EmailSenderConfig
from src.interface_adapters.file import File


class EmailSender(EmailSenderInterface):
    def __init__(self, config: EmailSenderConfig) -> None:
        self._config = config

    def send(self, recipient_email: str, subject: str, body: str, files: list[File]) -> None:
        msg = MIMEMultipart()
        msg["From"] = self._config.sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        for file in files:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.content)
            encoders.encode_base64(part)

            part.add_header("Content-Disposition", f'attachment; filename="{file.name}.pdf"')
            msg.attach(part)

        with smtplib.SMTP_SSL(self._config.sender_server, self._config.sender_port) as server:
            server.login(self._config.sender_email, self._config.sender_password)
            server.sendmail(self._config.sender_email, recipient_email, msg.as_string())
