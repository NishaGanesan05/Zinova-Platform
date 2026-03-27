import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["auth"])

# ── SMTP config from .env ─────────────────────────────────────────────────────
SMTP_SERVER   = os.getenv("BREVO_SMTP_SERVER", "smtp-relay.brevo.com")
SMTP_PORT     = int(os.getenv("BREVO_SMTP_PORT", "587"))
SMTP_LOGIN    = os.getenv("BREVO_EMAIL")
SMTP_PASSWORD = os.getenv("BREVO_PASSWORD")
SENDER_EMAIL  = os.getenv("BREVO_SENDER_EMAIL", SMTP_LOGIN)

# OTP store: { "user@email.com": "123456" }
otp_store = {}


def send_email(to_email: str, otp: str):
    """Send OTP email via SMTP"""
    print(f"[DEBUG] Sending OTP {otp} to {to_email}")
    print(f"[DEBUG] SMTP login: {SMTP_LOGIN}")
    print(f"[DEBUG] From (sender): {SENDER_EMAIL}")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Zinova OTP Code"
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = to_email

    body = MIMEText(
        f"Hello,\n\nYour Zinova verification code is:\n\n  {otp}\n\n"
        f"This code is valid for one use only.\n\nDo not share it with anyone.",
        "plain"
    )
    msg.attach(body)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
            print(f"[SUCCESS] Email sent to {to_email}")
    except Exception as e:
        print(f"[ERROR] Email failed: {e}")
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")


class EmailRequest(BaseModel):
    email: str


class VerifyRequest(BaseModel):
    email: str
    otp: str


@router.post("/send-otp")
def send_otp(body: EmailRequest):
    """Send OTP to user's email"""
    otp = str(random.randint(100000, 999999))
    otp_store[body.email] = otp
    print(f"[OTP] {body.email} → {otp}")

    send_email(body.email, otp)
    return {"message": "OTP sent to your email."}


@router.post("/verify-otp")
def verify_otp(body: VerifyRequest):
    """Verify OTP code"""
    stored = otp_store.get(body.email)

    if not stored:
        raise HTTPException(status_code=400, detail="No OTP found. Request a new one.")

    if stored != body.otp.strip():
        raise HTTPException(status_code=400, detail="Invalid OTP.")

    del otp_store[body.email]
    return {"message": "OTP verified successfully."}
