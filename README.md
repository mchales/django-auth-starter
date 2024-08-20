## Django Project Structure with Djoser User Auth and Simple JWT

This is a starter project for `django-rest-framework` applications using `djoser` and `djangorestframework-simplejwt` for user authentication. Folder structure is based off https://github.com/saqibur/django-project-structure/tree/master which has useful information.

Project includes

- Custom user class with corresponding admin panel
- API versioning with `rest_framework.versioning.NamespaceVersioning
- Automated testing (not extensive) with `pytest`
- Djoser authentication endpoints
- Simple JWT token blacklist endpoint (as Djoser doesn't blacklist token on logout)

Project does not include:

- Comprehensive testing
- Cron job to remove accounts which did not verify email, or other method to handle this edge case
- Cron job to remove expired and blacklisted tokens with `flushexpiredtokens`
- A frontend (apart from the one `django-rest-framework` provides)
- Docker configuration (will be added in the future)

## Getting Started

1. Clone this repository
2. Create python environment for project
   1. Using Conda `conda create --name your_env_name python=3.9`
3. Install packages to python environment:
   1. `pip install -r requirements/development.txt`
   2. If not using windows, remove pywin32==305 from development.txt
4. Populate `.env.development` file
   1. Generate secret key (see possible option below)
   2. Configure email SMTP host or disable Djoser email verification

```
from django.core.management.utils import get_random_secret_key SECRET_KEY = get_random_secret_key()
```

5. Run project with `python manage.py runserver`
6. Run `python manage.py migrate`
7. Run tests with `pytest`

## Extra

**Example Post Request**
`http://127.0.0.1:8000/api/v1/auth/users/`
Body:

```
{
    "email" : "example@gmail.com",
    "username": "example_name",
    "password" : "example_password",
    "re_password" : "example_password"
}
```

(I recommend using Postman and creating a Collection with auth endpoints)

## Configurations

Feel free to change the configurations to fit your needs.
For `djangorestframework-simple-jwt`

```
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',
}
```

For `djoser`

```
DJOSER = {
    'LOGIN_FIELD': 'username',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_ACTIVATION_EMAIL': True,
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_CONFIRMATION_EMAIL': True,
    'SERIALIZERS': {
        'user_create': f'apps.accounts.api.{DEFAULT_API_VERSION}.serializers.CustomUserCreateSerializer',
        'user': f'apps.accounts.api.{DEFAULT_API_VERSION}.serializers.CustomUserSerializer',
        'current_user': f'apps.accounts.api.{DEFAULT_API_VERSION}.serializers.CustomUserSerializer',
    },
}
```
