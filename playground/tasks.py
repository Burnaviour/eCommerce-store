
from time import sleep
from celery import shared_task


@shared_task
def notify_customers(message):
    print('sending')
    print(message)
    sleep(10)
    print("done sending email")
