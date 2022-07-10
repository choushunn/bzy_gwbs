# -*- coding: utf-8 -*-
# @Time    : 08/06/2021 16:15
# @Author  : Spring
# @FileName: urls.py
# @Software: PyCharm
from django.urls import path

from app.visual.views import UserAnswerShow

urlpatterns = [
    path('answer', UserAnswerShow.as_view()),
]
