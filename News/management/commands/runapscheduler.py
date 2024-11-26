import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from News.models import Post, Category
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.contrib.sites.models import Site


logger = logging.getLogger(__name__)

# немного модифицированная функция из сигналов
def weekly_email():

    # логика для домена сайта для добавления ссылки на публикацию
    current_site = Site.objects.get_current()
    domain = current_site.domain

    # отбираем публикации за промежуток понедельник-вскр
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    sunday = monday + timedelta(days=6)

    posts = Post.objects.filter(publication_date_gte=monday, publication_date_lte=sunday)

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

                    relative_url = post.get_absolute_url()  # относительная ссылка
                    full_url = f'http://{domain}{relative_url}'
                    message += f'" {post.title}". Читать по ссылке: {full_url}\n'
                message += '\n'

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


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            weekly_email,
            trigger=CronTrigger(day_of_week="sun", hour="23", minute="59"),  # публикуется почти в понедельник
            id="weekly_email",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_email'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="30"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")