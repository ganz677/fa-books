import smtplib

from celery import shared_task
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from starlette.templating import Jinja2Templates

from app.core.settings import settings


@shared_task
def send_confirmation_email(
    to_email: str,
    token: str,
) -> None:
    confirmation_url = f'http://127.0.0.1:8000/api/v1/auth/register_confirm?token={token}'
    
    templates = Jinja2Templates(directory=settings.front.templates_dir)
    template = templates.get_template(name="confirmation_email.html")
    html_content = template.render(confirmation_url=confirmation_url)

    text_content = f"Здравствуйте!\n\nДля подтверждения регистрации перейдите по ссылке:\n{confirmation_url}\n\nЕсли вы не регистрировались — просто проигнорируйте это письмо."

    message = MIMEMultipart("alternative")
    message["From"] = f"FaBooks <{settings.email.username}>"
    message["To"] = to_email
    message["Subject"] = "Подтверждение регистрации на FaBooks"

    message.attach(MIMEText(text_content, "plain", "utf-8"))
    message.attach(MIMEText(html_content, "html", "utf-8"))

    with smtplib.SMTP_SSL(
        host=settings.email.host,
        port=settings.email.port,
    ) as smtp:
        smtp.login(
            user=settings.email.username,
            password=settings.email.password.get_secret_value(),
        )
        smtp.send_message(message)
