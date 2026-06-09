import os
import smtplib
from email.message import EmailMessage
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def build_receipt_body(donation):
    return (
        f"Donation Receipt\n"
        f"==============================\n"
        f"Donation ID: {donation.id}\n"
        f"Donor: {donation.donor.username if donation.donor else 'Anonymous'}\n"
        f"Email: {donation.donor_email or (donation.donor.email if donation.donor else 'N/A')}\n"
        f"Phone: {donation.donor_phone or (donation.donor.phone if donation.donor else 'N/A')}\n"
        f"Orphanage: {donation.orphanage.name if donation.orphanage else 'N/A'}\n"
        f"Amount: ₹{donation.amount}\n"
        f"Type: {donation.donation_type or 'monetary'}\n"
        f"Payment Method: {donation.payment_method or 'N/A'}\n"
        f"Date: {donation.donation_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Status: {donation.status}\n"
        f"\nThank you for supporting this orphanage.\n"
    )


def send_email_slip(donation):
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    from_address = os.environ.get('SMTP_FROM', 'no-reply@orphanage.com')
    recipient = donation.donor_email or (donation.donor.email if donation.donor else None)

    if not smtp_server or not recipient:
        print(f"[notifications] Email slip not sent. SMTP_SERVER or recipient missing: smtp={smtp_server}, recipient={recipient}")
        return False

    message = EmailMessage()
    message['Subject'] = f"Donation Receipt #{donation.id}"
    message['From'] = from_address
    message['To'] = recipient
    message.set_content(build_receipt_body(donation))

    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            if smtp_username and smtp_password:
                server.login(smtp_username, smtp_password)
            server.send_message(message)
        print(f"[notifications] Email receipt sent to {recipient}")
        return True
    except Exception as exc:
        print(f"[notifications] Failed to send email receipt: {exc}")
        return False


def send_sms_slip(donation):
    phone = donation.donor_phone or (donation.donor.phone if donation.donor else None)
    if not phone:
        print(f"[notifications] SMS slip not sent. No phone number available for donation {donation.id}.")
        return False

    sms_api_url = os.environ.get('SMS_API_URL')
    sms_api_key = os.environ.get('SMS_API_KEY')
    sms_from = os.environ.get('SMS_FROM')

    body = build_receipt_body(donation)
    summary = f"Donation ID {donation.id}: ₹{donation.amount} received. Thank you!"

    if sms_api_url and sms_api_key:
        payload = {
            'api_key': sms_api_key,
            'from': sms_from or '',
            'to': phone,
            'message': summary
        }
        request = Request(sms_api_url, data=urlencode(payload).encode('utf-8'), method='POST')
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        try:
            response = urlopen(request, timeout=10)
            print(f"[notifications] SMS receipt sent to {phone}. Response code: {response.getcode()}")
            return True
        except (HTTPError, URLError) as exc:
            print(f"[notifications] Failed to send SMS receipt: {exc}")
            return False

    print(f"[notifications] SMS receipt ready for {phone}. No SMS service configured.")
    return False


def notify_donation_slip(donation):
    email_sent = send_email_slip(donation)
    sms_sent = send_sms_slip(donation)
    return {
        'email_sent': email_sent,
        'sms_sent': sms_sent
    }
