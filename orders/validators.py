import re
from django.core.exceptions import ValidationError


regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def validate_order(request_data):
    if not re.match("([A-Z0-9]{2})-([A-Z0-9]{2})", request_data['robot_serial']):
            raise ValidationError('Формат серии робота должен быть XX-XX (две пары букв и(или) цифр)')
    if not re.fullmatch(regex_email, request_data['customer_email']):
            raise ValidationError('Не корркетный email')
    return request_data