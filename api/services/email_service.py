import os
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr
from typing import Optional, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class EmailService:
    """Service for sending SMTP emails."""
    
    def __init__(self):
        """Initialize email configuration."""
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_name = "Jeet Majumder"
        self.sender_email = "jeet0912majumder@gmail.com"
        self.sender_password = os.getenv("SENDER_PASSWORD")
        
        if not self.sender_password:
            raise ValueError("SENDER_PASSWORD must be set in environment variables")
    
    def _create_email_content(self, name: str, subject: str, message: str) -> Tuple[str, str]:
        """
        Create plain text and HTML email content.
        
        Args:
            name: Recipient's name
            subject: Message subject
            message: Message content
            
        Returns:
            Tuple of (plain_text_content, html_content)
        """
        # Plain text content
        text_content = f"""
        Hello {name},

        Thank you for visiting my web portfolio.

        I have received your message and appreciate the time you took to write.
        I will review your message and get back to you as soon as possible.

        For your reference, here is a copy of your message:

        Subject: {subject}

        Message:
        {message}

        Kind regards,
        Jeet Majumder
        """
        
        # HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Thank you for contacting me</title>
        </head>
        <body style="
            margin: 0;
            padding: 0;
            background-color: #f2f5f9;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            color: #2c3e50;
        ">
            <table width="100%" cellpadding="0" cellspacing="0" style="padding: 24px 0;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="
                            background-color: #ffffff;
                            border-radius: 10px;
                            overflow: hidden;
                            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
                        ">

                            <!-- Header -->
                            <tr>
                                <td style="
                                    background: linear-gradient(135deg, #1f3c88, #3a7bd5);
                                    padding: 22px 26px;
                                    color: #ffffff;
                                ">
                                    <h1 style="
                                        margin: 0;
                                        font-size: 22px;
                                        font-weight: 600;
                                    ">
                                        Thanks for Getting in Touch
                                    </h1>
                                </td>
                            </tr>

                            <!-- Body -->
                            <tr>
                                <td style="padding: 26px;">
                                    <p style="font-size: 15px; margin-top: 0;">
                                        Hello <strong>{name}</strong>,
                                    </p>

                                    <p style="font-size: 15px; line-height: 1.6;">
                                        Thank you for visiting my web portfolio.
                                    </p>

                                    <p style="font-size: 15px; line-height: 1.6;">
                                        I have received your message and appreciate the time you took to write.
                                        I will review your message and get back to you as soon as possible.
                                    </p>

                                    <p style="font-size: 14px; line-height: 1.6; color: #6b7280;">
                                        For your reference, here is a copy of your message:
                                    </p>

                                    <!-- Message Card -->
                                    <div style="
                                        margin: 22px 0;
                                        padding: 18px;
                                        background-color: #f8fafc;
                                        border-radius: 8px;
                                        border-left: 4px solid #3a7bd5;
                                    ">
                                        <p style="margin: 0 0 8px 0; font-size: 14px;">
                                            <strong>Subject:</strong> {subject}
                                        </p>

                                        <p style="
                                            margin: 0;
                                            font-size: 14px;
                                            line-height: 1.6;
                                            white-space: pre-line;
                                        ">
                                            {message}
                                        </p>
                                    </div>

                                    <p style="margin-bottom: 0; font-size: 14px;">
                                        Kind regards,<br>
                                        <strong>Jeet Majumder</strong>
                                    </p>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="
                                    padding: 14px 26px;
                                    background-color: #f2f5f9;
                                    font-size: 12px;
                                    color: #6b7280;
                                    text-align: center;
                                ">
                                    This is an automated acknowledgment from Jeet Majumder's portfolio website.
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        return text_content, html_content
    
    def send_auto_reply(self, recipient_email: str, name: str, subject: str, message: str) -> bool:
        """
        Send an auto-reply email to the contact form submitter.
        
        Args:
            recipient_email: Email address of the person who submitted the form
            name: Name of the person
            subject: Subject of their message
            message: Their message content
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Create email message
            msg = EmailMessage()
            msg['Subject'] = "Thank you for reaching out"
            msg['From'] = formataddr((self.sender_name, self.sender_email))
            msg['To'] = recipient_email
            
            # Create content
            text_content, html_content = self._create_email_content(name, subject, message)
            
            # Set content
            msg.set_content(text_content)
            msg.add_alternative(html_content, subtype='html')
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


# Create a singleton instance
email_service = EmailService()

