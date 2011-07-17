from django.test import TestCase
from django.core.urlresolvers import reverse


class ProfileTests(TestCase):
    """ Test /profile REST interface """

    def test_profile_post_new(self):
        cipher_text = '~~27b245de082bf9e3'
        data = {
            'username': 'sergray@gmail.com',
            'portrait': 'https://odesk-prod-portraits.s3.amazonaws.com/Users:sergray:PortraitUrl?AWSAccessKeyId=1XVAX3FNQZAFC9GJCFR2&Expires=2147483647&Signature=gGqkxBncnilW8ZrS1Aqm6TOs3NA%3D',
        }
        url = reverse('profile-resource', kwargs={'cipher_text': cipher_text})
        self.client.post(url, data)
        self.client.get(url)
