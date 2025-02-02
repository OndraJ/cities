from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


def confirm_email(request, user):
    token = TokenGenerator().make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    confirmation_path = reverse(
        "accounts:email_confirm", kwargs={"uidb64": uidb64, "token": token}
    )
    confirmation_url = f"{request.scheme}://{request.get_host()}{confirmation_path}"

    email_subject = "Activate your account"
    email_body = (
        f"Dear {user.username}, \n"
        f"Please confirm your email address: {user.email} to activate your account. \n"
        f"Click the link below to confirm your email address: \n"
        f"{confirmation_url}"
    )
    # email_body = """
    # Dear {user.username},
    # Please confirm your email address: {user.email} to activate your account.
    # <a href="{confirmation_url}">Confirm email address</a>
    # If you did not register for an account, please ignore this email.
    # """
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=[user.email],
    )
    # email.content_subtype = "html"
    email.send(fail_silently=False)
