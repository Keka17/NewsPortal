
from django.db import transaction
from django.db.models.signals import post_save, m2m_changed
from allauth.account.signals import user_signed_up, email_confirmed

from django.dispatch import receiver
from .models import Post
from django.core.mail import send_mail
from django.contrib.sites.models import Site

from .tasks import new_post_notification


# send_post_notification.delay(instance.id) — асинхронный вызов задачи

# отслеживание изменение в поле M2M
@receiver(m2m_changed, sender=Post.category.through)
def category_changed(sender, instance, action, **kwargs):
    if action == "post_add":
        transaction.on_commit(lambda: new_post_notification.delay(instance.id))  # celery не работает напрямую с объектами Dj


@receiver(email_confirmed)
def welcome_message(sender, request, email_address, **kwargs):
    user = email_address.user
    subject = 'Регистрация на сайте News Portal'
    message = (f'❤️Спасибо за регистрацию на нашем сайте, {user.username}!\n'
               f'Приятного чтения 🥰')

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='charliebrownkb3@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        print(f'Письмо успешно отправлено {user.email}')
    except Exception as e:
        print(f'Ошибка при отправке письма {user.email}: {e}')