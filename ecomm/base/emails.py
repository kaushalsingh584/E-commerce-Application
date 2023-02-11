from django.conf import settings
from django.core.mail import send_mail


def send_email_verification_link(email, email_token ):
    print("reached")
    subject  = "Your account needs to be verified"
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, click on the link to activate your account http://localhost:8000/accounts/activate/{email_token}'
    send_mail(subject , message , email_from , [email])
    print("mail send")
