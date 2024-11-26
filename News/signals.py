
from django.db import transaction
from django.db.models.signals import post_save, m2m_changed
from allauth.account.signals import user_signed_up, email_confirmed

from django.dispatch import receiver
from .models import Post
from django.core.mail import send_mail
from django.contrib.sites.models import Site

# instance - только что сохраненный объект модели sender
@receiver(post_save, sender=Post)
def send_notification(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: mail(instance))  # сигнал выполнится после всех изменений в БД

# отслеживание изменение в поле M2M
@receiver(m2m_changed, sender=Post.category.through)
def category_changed(sender, instance, action, **kwargs):
    if action == "post_add":  # проверка на добавление категорий
        mail(instance)

# принты делала для удобства проверки
def mail(instance):

    # логика для домена сайта для добавления ссылки на публикацию
    current_site = Site.objects.get_current()
    domain = current_site.domain

    all_categories = ', '.join(category.category_name for category in instance.category.all())
    categories_count = instance.category.count()

    section_intro = (
        "Новая публикация в твоем любимом разделе"
        if categories_count == 1
        else "Новая публикация в твоих любимых разделах"
    )

    for category in instance.category.all():
        # print(f'Категория: {category.category_name}')
        subscribers = category.subscribers.all()
        # print(f'Подписчики категории: {[subscriber.email for subscriber in subscribers]}')

        for subscriber in subscribers:
            relative_url = instance.get_absolute_url()  # относительная ссылка
            full_url = f'http://{domain}{relative_url}'

            subject = f'{instance.title}'
            message = (
                f'👋 Здравствуй, {subscriber.username}!\n\n'
                f'{section_intro}: {all_categories}\n\n'
                f'{instance.text[:200]}...\n\n'
                f'Читай польностью по ссылке: {full_url}'
            )
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='charliebrownkb3@gmail.com',
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
                print(f'Письмо успешно отправлено {subscriber.email}')
            except Exception as e:
                print(f'Ошибка при отправке письма {subscriber.email}: {e}')


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