from .models import staffAccount
import pyotp
import requests

# auth_app/services.pyy


def getUserService(request):

    try:
        uuid = request.data.get('uuid', None)
        user = staffAccount.objects.get(uuid=uuid)
        return user
    except:
        return None


def getQRCodeService(user):

    email = user.email.lower()
    otp_base32 = pyotp.random_base32()
    otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
        name=email, issuer_name="SAMS(Ostram)")

    user.otp_base32 = otp_base32
    user.is_authenticator = True
    user.save()

    return otp_auth_url


def getOTPValidityService(user, otp):

    totp = pyotp.TOTP(user.otp_base32)
    if not totp.verify(otp):
        return False
    user.logged_in = True
    user.save()
    return True
