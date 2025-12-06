from twilio.rest import Client
from backend.config import settings

class TwilioService:
    def __init__(self):
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        else:
            self.client = None

    def send_whatsapp_message(self, to_number: str, body_text: str):
        """
        Sends a WhatsApp message.
        to_number: The user's phone number as received from Twilio (e.g. 'whatsapp:+1234567890')
        """
        if not self.client:
            print(f"[MOCK] Sending WhatsApp to {to_number}: {body_text}")
            return

        from_number = settings.TWILIO_WHATSAPP_NUMBER or "whatsapp:+14155238886"
        
        try:
            message = self.client.messages.create(
                from_=from_number,
                body=body_text,
                to=to_number
            )
            return message.sid
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return None

twilio_service = TwilioService()
