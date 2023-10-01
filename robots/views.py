import xlsxwriter
import pandas as pd
from pytz import timezone
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from django.core.serializers import serialize

from .models import Robot

FILEPATH = "robots_report.xlsx"

moscow_tz = timezone('Europe/Moscow')
current_week = moscow_tz.localize(datetime.now()).isocalendar()[1]

class RobotView(View):

    def get(self, request):
        robots_made = Robot.objects.filter(created__week=current_week)
        robots_made = [[robot.model, robot.version, robot.serial] for robot in robots_made]
        df = pd.DataFrame(robots_made, columns=['Модель', 'Версия', 'Количество за неделю'])
        models_list = df.Модель.unique()
        df = pd.pivot_table(df,values='Количество за неделю', index=['Модель', 'Версия'], aggfunc='count')
        with pd.ExcelWriter(FILEPATH, engine='xlsxwriter') as writer:
            [df.filter(like=model, axis=0).to_excel(writer, startrow=1, startcol=1,
                                                     sheet_name='Модель '+model) for model in models_list]
            [value.autofit() for key, value in writer.sheets.items()]
        return JsonResponse({'report': f'Произведено роботов на текущей неделе: {len(robots_made)} шт.\
                                         Отчет сформирован'},
                             json_dumps_params={'ensure_ascii': False},
                             content_type='application/json; charset=utf-8')
        