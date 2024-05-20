import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from data_statistics.models import MailingStat
from mailing.models import Mailing, Message

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)


def check_status(mailing):
    if mailing.time_start <= timezone.now().time() <= mailing.time_stop:
        mailing.status = "LA"
    elif mailing.time_stop < timezone.now().time():
        mailing.status = "CP"
    elif timezone.now().time() < mailing.time_start:
        mailing.status = "PA"
    mailing.save()
    logger.info("check_status done!")


def sending_mailing(mailing):
    messages = Message.objects.filter(mailing=mailing).filter(is_active=True)
    clients = mailing.client_set.all()
    if messages and clients:
        try:
            send_mail(
                subject=messages[0].title,
                message=messages[0].body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in clients],
            )
        except Exception as error:
            mailing_stat = MailingStat.objects.create(
                name=f"Error {mailing.name}", response=error, mailing=mailing, status_attempt=False
            )
            mailing_stat.save()

        else:
            mailing_stat = MailingStat.objects.create(
                name=f"OK {mailing.name}", response="OK", mailing=mailing, status_attempt=True
            )
            mailing_stat.save()
    logger.info("sending_mailing done!")


def check_jobs():
    for mailing in Mailing.objects.all():
        check_status(mailing)
        print(mailing.name, MailingStat.objects.filter(mailing=mailing).exists())
        if not MailingStat.objects.filter(mailing=mailing).exists():
            add_job_mailing(mailing)
            MailingStat.objects.create(
                name=f"Pause {mailing.name}", response="Pause", mailing=mailing, status_attempt=False
            )
    logger.info("Check_jobs done!")


def add_job_mailing(mailing):
    if mailing.periodicity == "DAY":
        period = CronTrigger(hour=mailing.time_start.hour, minute=mailing.time_start.minute)
    elif mailing.periodicity == "WEEK":
        period = CronTrigger(
            day_of_week=datetime.weekday(mailing.datetime_created),
            hour=mailing.time_start.hour,
            minute=mailing.time_start.minute,
        )
    else:
        period = CronTrigger(
            day=mailing.datetime_created.day, hour=mailing.time_start.hour, minute=mailing.time_start.minute
        )

    scheduler.add_job(
        sending_mailing,
        trigger=period,
        id=f"Mailing {mailing.pk}",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        args=[mailing],
        replace_existing=True,
    )
    logger.info("add_job done!")


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
        trigger=CronTrigger(minute="*/10"),  # Every 10 minutes
        id="check_jobs",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'check_jobs'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added weekly job: 'delete_old_job_executions'.")

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
