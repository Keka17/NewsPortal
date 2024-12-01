from celery import shared_task
from News.models import Post, Category
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.contrib.sites.models import Site
import logging

logger = logging.getLogger(__name__)


def send_email(subscriber, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='charliebrownkb3@gmail.com',
            recipient_list=[subscriber.email],
            fail_silently=False,
        )
        logger.info(f'Письмо успешно отправлено {subscriber.email}')
        return True
    except Exception as e:
        logger.exception(f'Ошибка при отправке письма {subscriber.email}: {e}')
        return False


@shared_task
def weekly_email():

    # логика для домена сайта для добавления ссылки на публикацию
    current_site = Site.objects.get_current()
    domain = current_site.domain

    # отбираем публикации за промежуток понедельник-вскр
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    sunday = monday + timedelta(days=6)

    posts = Post.objects.filter(publication_date_gte=monday, publication_date_lte=sunday)

    success_count = 0
    failure_count = 0

    for category in Category.objects.all():
        subscribers = category.subscribers.all()

        for subscriber in subscribers:
            subscriber_posts = posts.filter(category=category)

            if subscriber_posts:
                subject = 'Публикации за прошедшую неделю'
                message = (
                    f'✊ Здравствуй, {subscriber.username}!\n'
                    f'Вот публикации в разделе "{category.category_name}" за прошедшую неделю:\n'
                )
                for post in subscriber_posts:
                    relative_url = post.get_absolute_url()
                    full_url = f'http://{domain}{relative_url}'
                    message += f'" {post.title}". Читать по ссылке: {full_url}\n'
                message += '\n'

                if send_email(subscriber, subject, message):
                    success_count += 1
                else:
                    failure_count += 1

            logger.info(f"Еженедельная рассылка закончилась. "
                        f"Количество отправленных писем: {success_count}, "
                        f"количество неотправленных писем: {failure_count}")
            return {'success': success_count, 'failure': failure_count}


@shared_task
def new_post_notification(post_id):
    try:
        post = Post.objects.get(pk=post_id)
        current_site = Site.objects.get_current()
        domain = current_site.domain
        all_categories = ', '.join(category.category_name for category in post.category.all())
        categories_count = post.category.count()
        section_intro = (
            "Новая публикация в твоем любимом разделе"
            if categories_count == 1
            else "Новая публикация в твоих любимых разделах"
        )

        for category in post.category.all():
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                relative_url = post.get_absolute_url()
                full_url = f'http://{domain}{relative_url}'
                subject = f'{post.title}'
                message = (
                    f'👋 Здравствуй, {subscriber.username}!\n\n'
                    f'{section_intro}: {all_categories}\n\n'
                    f'{post.text[:200]}...\n\n'
                    f'Читай полностью по ссылке: {full_url}'
                )
                send_email(subscriber, subject, message)
    except Exception as e:
        logger.exception(f"Error processing post notification for post {post_id}: {e}")




