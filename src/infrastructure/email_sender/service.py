import smtplib
from dataclasses import dataclass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import FastAPI, HTTPException, UploadFile

from src.dto.file import File
from src.infrastructure.email_sender.config import EmailSenderConfig


class EmailSender:
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

            # Correct Content-Disposition with filename
            part.add_header("Content-Disposition", f'attachment; filename="{file.name}.pdf"')
            msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com", 587)  # Замените на ваш SMTP сервер
        server.starttls()
        server.login(self._config.sender_email, self._config.sender_password)
        text = msg.as_string()
        server.sendmail(self._config.sender_email, recipient_email, text)
        server.quit()
