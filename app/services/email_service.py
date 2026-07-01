from flask import url_for
from flask_mail import Message

from app.extensions import mail


def send_verification_email(user, token):
    verification_url = url_for("auth.verify_email", token=token, _external=True)

    try:
        msg = Message(
            subject="Verify your Wellbeing Quest account",
            recipients=[user.email],
        )
        msg.body = f"""Hello {user.full_name},

Welcome to Wellbeing Quest.

Please verify your email by clicking this link:

{verification_url}

If you did not create this account, you can safely ignore this email.
"""
        mail.send(msg)
        return True
    except Exception as error:
        print("\nEMAIL COULD NOT BE SENT")
        print(error)
        print("Development verification link:")
        print(verification_url)
        return False
