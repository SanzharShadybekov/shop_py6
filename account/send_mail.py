from django.core.mail import send_mail
from decouple import config

HOST = config('HOST')


def send_confirm_email(user, code):
    link = f'{HOST}/api/v1/accounts/activate/{code}/'
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Чтобы активировать ваш аккаунт нужно перейти по ссылке ниже:'
        f'\n{link}'
        f'\nСсылка работает один раз!',
        'johnsnowtest73@gmail.com',
        [user],
        fail_silently=False,
    )
