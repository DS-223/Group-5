import smtplib, pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import text

class EmailCampaignManager:
    """
    Manages email campaigns targeted at specific RFM customer segments.
    Automatically loads and sends appropriate email templates based on the segment.
    """

    email_templates = {
        "Champions": {
            "subject": "You're a Champion – Thank You for Your Loyalty!",
            "body": """\
                Hi there,
                We just wanted to say a huge THANK YOU for being one of our most valued customers. Your consistent support means the world to us!
                🎁 As a token of appreciation, here’s a 25% discount code: CHAMP25
                Keep shining,  
                The Marketing Enthusiasts Team
                """
                },
        "Loyal Customers": {
            "subject": "You’re One of Our Favorite Customers 💙",
            "body": """\
                Hello!
                e’ve noticed your loyalty, and we’re so grateful to have you with us. You’re part of what keeps our business thriving.
                💡 Here's a little something for you: LOYAL15 – 15% off your next order.
                Thanks for sticking with us!  
                Warm regards,  
                Marketing Enthusiasts Team
                """
                },
        "Potential Loyalists": {
            "subject": "Let’s Take This to the Next Level 🚀",
            "body": """\
                Hey there,
                You've shown interest and we're excited to see where this goes. We'd love to become your go-to choice.
                🎁 Try us again with this 10% discount: WELCOME10
                Looking forward to having you back,  
                Marketing Enthusiasts Team
                """
                },
        "Leaving Customers": {
            "subject": "We Miss You – Come Back for a Special Offer",
            "body": """\
                Hi,
                It looks like we haven’t seen you in a while. We’d really love to have you back!
                💡 Here’s 20% off your next purchase: COMEBACK20
                Let us know how we can do better. We're always listening.
                Best,  
                Marketing Enthusiasts Team
                """
                },
        "Big Spenders": {
            "subject": "You're VIP to Us 💸",
            "body": """\
                Hello [Customer],
                We noticed you’ve been making big moves — and we think that’s awesome.
                🌟 As a top spender, you get early access to new products and special rewards. Here’s 30% off your next order: VIP30
                Thanks for being amazing,  
                Marketing Enthusiasts Team
                """
                }
    }

    def __init__(self, segment: str, engine, sender_email: str, app_password: str):
        if segment not in self.email_templates:
            raise ValueError(f"Unsupported segment: {segment}")
        self.segment      = segment
        self.engine       = engine
        self.sender_email = sender_email
        self.app_password = app_password
        self.smtp_server  = "smtp.gmail.com"
        self.smtp_port    = 587
        self.emails: list[str] = []

    def fetch_emails(self) -> int:
        """
        Pull every non-null e-mail that belongs to this segment.
        """
        sql = text("""
            SELECT dc."Email"
            FROM   "DimCustomer"  dc
            JOIN   "RFMResults"   r
                   ON CAST(dc."CustomerCardCode" AS BIGINT) = r."card_code"
            WHERE  lower(r."segment") = :seg
              AND  dc."Email" IS NOT NULL
        """)
        df = pd.read_sql(sql, self.engine, params={"seg": self.segment.lower()})
        self.emails = df["Email"].dropna().unique().tolist()
        return len(self.emails)

    # ------------------------------------------------------------------ #
    def send_emails(self):
        """
        Send the template to everyone in self.emails
        (call inside a BackgroundTask).
        """
        if not self.emails:
            raise RuntimeError("fetch_emails() first – no addresses loaded")

        tpl = self.email_templates[self.segment]
        subject, body = tpl["subject"], tpl["body"]

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.app_password)

            for addr in self.emails:
                msg = MIMEMultipart()
                msg["From"] = self.sender_email
                msg["To"] = addr
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                try:
                    server.send_message(msg)
                    print(f"✓  sent to {addr}")
                except Exception as exc:
                    print(f"✗  {addr}: {exc}")
