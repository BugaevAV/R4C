import json
import re
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .validators import *
from .models import Robot


@method_decorator(csrf_exempt, name='dispatch')
class RobotView(View):

    def post(self, request):
        request_body = json.loads(request.body)
        validated_robot_data = {
            'model': validate_serial(request_body.get('model')),
            'version': validate_serial(request_body.get('version')),
            'serial': request_body.get('model') + "-" + request_body.get('version'),
            'created': validate_creation_data(request_body.get('created'))
        }
        robot_obj = Robot.objects.create(**validated_robot_data)      
        return JsonResponse({'Cоздан робот': {"model":robot_obj.model,
                                              "version":robot_obj.version,
                                              "created":robot_obj.created}},
                                               json_dumps_params={'ensure_ascii': False},
                                               content_type='application/json; charset=utf-8')
        