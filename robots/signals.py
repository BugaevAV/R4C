from django.dispatch import Signal
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


robot_is_made = Signal()

MESSAGE = """Добрый день!\nНедавно Вы интересовались нашим роботом модели %s, версии %s. Этот робот теперь в наличии.
             Если Вам подходит этот вариант - пожалуйста, свяжитесь с нами"""


@receiver(robot_is_made)
def mail_to_customer(customer_email, robot_serial, order_id, **kwargs):
    msg = EmailMultiAlternatives(f"Статус заказа робота серии {robot_serial}",
                                  MESSAGE % (robot_serial[:2], robot_serial[3:]),
                                  settings.EMAIL_HOST_USER,
                                  [customer_email])
    print(f"Обновлен статус заказа #{order_id}, для {customer_email}. Письмо отправлено.")
    msg.send()
    