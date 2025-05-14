from email_sender import EmailSender


def main() -> None:
    sender = EmailSender()
    recipient = 'example@example.com'
    subject = 'asd'
    body = 'asd'
    sender.send(
        recipient=recipient,
        subject=subject,
        body=body,
    )



if __name__ == '__main__':
    main()
