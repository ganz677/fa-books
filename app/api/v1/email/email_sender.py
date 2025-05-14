import logging

log = logging.getLogger(__name__)

class EmailSender:
    # def __init__(self):
    #     pass

    def send(self,
             recipient: str,
             subject: str,
             body: str,
    ) -> None:
        log.info(
            'Sending email to %r with subject %r and body %r',
            recipient,
            subject,
            body,
        )
