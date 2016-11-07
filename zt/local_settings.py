DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zavod',
        'USER': 'zavod_user',
        'PASSWORD': 'zavod',
        'HOST': 'localhost',
        'PORT': '',
   }
}

# Email

EMAIL_HOST_USER = 'm.g.zubareva@gmail.com'
EMAIL_HOST_PASSWORD = 'Maxspntvdw8'

EMAILS_FOR_FAQ = ['ria6@yandex.ru']
EMAILS_FOR_CALLBACK = ['ria6@yandex.ru']

SOCIAL_AUTH_VK_OAUTH2_KEY = '5617940'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'qBU9sjCXLjaOikzmsDYs'

SOCIAL_AUTH_FACEBOOK_KEY = '920189241442699'
SOCIAL_AUTH_FACEBOOK_SECRET = '5bbe0790fdc569cbb8f81ee51116e82c'

SOCIAL_AUTH_TWITTER_KEY = '62VEZJXsizBzviROtplTiwABm'
SOCIAL_AUTH_TWITTER_SECRET = 'jGiXRTbTjZHtdT48MUd4XSpmDSRpXta9YGLzfp5BwPv2z7q08t'
