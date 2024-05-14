import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.utils import timezone
from django.core.mail import send_mail

from data_statistics.models import MailingStat
from mailing.models import Mailing, Message

logger = logging.getLogger(__name__)
scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)


def check_status(mailing):
    if mailing.time_start <= timezone.now().time() <= mailing.time_stop:
        mailing.status = 'LA'
    elif mailing.time_stop < timezone.now().time():
        mailing.status = 'CP'
    elif timezone.now().time() < mailing.time_start:
        mailing.status = 'PA'
    mailing.save()
    logger.info("check_status done!")
    print('check_status')


def sending_mailing(mailing):
    messages = Message.objects.filter(mailing=mailing).filter(is_active=True)
    clients = mailing.client_set.all()
    # if messages and clients:
    #     try:
    #
    #         send_mail(
    #             subject=messages[0].title,
    #             message=messages[0].body,
    #             from_email=settings.EMAIL_HOST_USER,
    #             recipient_list=[client.email for client in clients],
    #         )
    #     except Exception as error:
    #         mailing_stat = MailingStat.objects.create(name=f"Error {mailing.name}", response=error, mailing=mailing)
    #         mailing_stat.save()
    #
    #     else:
    #         mailing_stat = MailingStat.objects.create(name=f"OK {mailing.name}", response='OK', mailing=mailing)
    #         mailing_stat.save()
    logger.info("sending_mailing done!")
    print(mailing.name, messages, clients)


def check_jobs():
    for mailing in Mailing.objects.all():
        check_status(mailing)
        if not MailingStat.objects.filter(mailing=mailing).exists():
            add_job(mailing)
    logger.info('Check_jobs done!')
    print('check_jobs')


def add_job(mailing):
    if mailing.periodicity == 'DAY':
        period = CronTrigger(second="*/10")
    elif mailing.periodicity == 'WEEK':
        period = CronTrigger(second="*/20")
    else:
        period = CronTrigger(second="*/30")

    scheduler.add_job(
        sending_mailing,
        trigger=period,
        id=f"Mailing {mailing.pk}",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        args=[mailing],
        replace_existing=True,
    )
    logger.info("add_job done!")
    print('add_job')


@util.close_old_connections
def delete_old_job_executions(max_age=2_628_000):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def start_scheduler():
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        check_jobs,
        trigger=CronTrigger(second="*/5"),  # Every 5 second
        id="check_jobs",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'check_jobs'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),
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
