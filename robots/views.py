import json
import re
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .validators import *
from .models import Robot
from orders.models import Order
from .signals import robot_is_made


@method_decorator(csrf_exempt, name='dispatch')
class RobotView(View):

    def post(self, request):
        request_body = json.loads(request.body)
        validated_robot_data = {
            'model': validate_robot_version_model(request_body.get('model')),
            'version': validate_robot_version_model(request_body.get('version')),
            'serial': request_body.get('model') + "-" + request_body.get('version'),
            'created': request_body.get('created')
        }
        robot_obj = Robot.objects.create(**validated_robot_data)
        check_orders = Order.objects.filter(robot_serial=validated_robot_data['serial'])
        if check_orders:
            customer_email = check_orders.first().customer.email
            order_id = check_orders.first().pk  
            robot_is_made.send(sender=None, customer_email=customer_email ,
                                robot_serial=robot_obj.serial, order_id=order_id)     
        return JsonResponse({'Cоздан робот': {"model":robot_obj.model,
                                              "version":robot_obj.version,
                                              "created":robot_obj.created}},
                                               json_dumps_params={'ensure_ascii': False},
                                               content_type='application/json; charset=utf-8')
        