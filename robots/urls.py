from django.urls import path

from .views import RobotView

urlpatterns = [
    path('report/', RobotView.as_view()),
]
