import json
import time
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


from .validators import validate_order
from .models import Order
from customers.models import Customer
from robots.models import Robot



@method_decorator(csrf_exempt, name='dispatch')
class OrderView(View):

    def post(self, request):
        request = validate_order(json.loads(request.body))
        customer, _ = Customer.objects.get_or_create(email=request['customer_email'])
        order = customer.order_set.create(robot_serial=request['robot_serial'])  #получили заказ
        check_warehouse = Robot.objects.filter(serial=request['robot_serial'])   #проверили склад
        order_id = order.id
        if check_warehouse:                                      #Если робот в наличиии удалили заказ и робота из базы =
            time.sleep(2)                                        # = скоплектовали и отправли заказ = изменили состояние базы роботов и заказов                 
            check_warehouse.first().delete()                     #Необходимо для корретной проверки наличия и отправки ПИСЬМА по сигналу
            print(f'Заказ #{order_id} скомплектован и отправлен')#в приложении robots
            time.sleep(2)
            order.delete()                                                    
            return JsonResponse ({f'Выполнен заказ #{order_id}': f"серия робота {order.robot_serial}, заказчик {customer.email}"},
                                                                                        json_dumps_params={'ensure_ascii': False},
                                                                                  content_type='application/json; charset=utf-8')                  
        return JsonResponse ({f'Cоздан заказ #{order.id}': f"серия робота {order.robot_serial}, заказчик {customer.email}.\
                              В данный момент робота нет в наличии"}, json_dumps_params={'ensure_ascii': False},
                                                                      content_type='application/json; charset=utf-8')
 