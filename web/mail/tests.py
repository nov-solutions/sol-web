import os

from django.conf import settings
from django.core import mail
from django.test import TestCase, override_settings
from mail.utils import send_verification_email

DEFAULT_FROM_EMAIL = "Django Test <automated@django.test.net>"


class DummyUser:
    def __init__(self, email, magic_link_url):
        self.email = email
        self.magic_link_url = magic_link_url


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL=DEFAULT_FROM_EMAIL,
)
class LocmemEmailBackendTest(TestCase):
    def test_send_verification_email(self):
        user = DummyUser("test@example.com", "http://example.com/verify")
        send_verification_email(user)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        # Check contents of the email
        self.assertEqual(email.subject, "Verify your account")
        self.assertEqual(email.from_email, DEFAULT_FROM_EMAIL)
        self.assertEqual(email.to, [user.email])
        self.assertIn(user.magic_link_url, email.body)


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.filebased.EmailBackend",
    EMAIL_FILE_PATH="/tmp/dummy-mail",
    DEFAULT_FROM_EMAIL=DEFAULT_FROM_EMAIL,
)
class FileBasedEmailBackendTest(TestCase):
    def setUp(self):
        # empty tmp email dir
        email_dir = settings.EMAIL_FILE_PATH
        if os.path.exists(email_dir):
            for f in os.listdir(email_dir):
                os.remove(os.path.join(email_dir, f))
        else:
            os.makedirs(email_dir)

    def test_send_verification_email_file_backend(self):
        user = DummyUser("test@example.com", "http://example.com/verify")
        send_verification_email(user)
        # List the files in the EMAIL_FILE_PATH directory.
        files = os.listdir(settings.EMAIL_FILE_PATH)
        self.assertEqual(len(files), 1)
        file_path = os.path.join(settings.EMAIL_FILE_PATH, files[0])
        with open(file_path, "r") as f:
            email_content = f.read()

        # check contents of the email
        self.assertIn("Verify your account", email_content)
        self.assertIn(user.email, email_content)
        self.assertIn(user.magic_link_url, email_content)
        self.assertIn(DEFAULT_FROM_EMAIL, email_content)
