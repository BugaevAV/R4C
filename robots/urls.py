from django.urls import path

from .views import RobotView

urlpatterns = [
    path('robot/', RobotView.as_view()),
]