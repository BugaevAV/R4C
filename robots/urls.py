from django.urls import path

from .views import RobotView

urlpatterns = [
    path('create/', RobotView.as_view()),
]