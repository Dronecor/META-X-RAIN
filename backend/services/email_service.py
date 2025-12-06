import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from backend.config import settings

class EmailService:
    def __init__(self):
        if settings.SENDGRID_API_KEY:
            self.sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        else:
            self.sg = None

    def send_email(self, to_email: str, subject: str, html_content: str):
        if not self.sg:
            print(f"[MOCK] Sending Email to {to_email}: {subject}")
            return

        from_email = Email("noreply@agenticcrm.com") # Should be configured
        to_email = To(to_email)
        content = Content("text/html", html_content)
        
        mail = Mail(from_email, to_email, subject, content)
        
        try:
            response = self.sg.client.mail.send.post(request_body=mail.get())
            return response.status_code
        except Exception as e:
            print(f"Error sending email: {e}")
            return None

email_service = EmailService()
