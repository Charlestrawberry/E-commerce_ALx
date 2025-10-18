
from .celery import app
from django.core.mail import send_mail

@app.task
def send_order_confirmation(order_id):
    # get order, send email to user
    pass
