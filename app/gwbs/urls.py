# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 12:31
# @Author  : Spring
# @FileName: urls.py
# @Software: PyCharm
from django.urls import path

from app.gwbs.views import IndexView, LoginView, Uploader, InfoView, OverView, display_meta

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('gwbs', IndexView.as_view(), name="index"),
    path('info', InfoView.as_view(), name="info"),
    path('over', OverView.as_view(), name="over"),
    path('uploader', Uploader.as_view(), name="uploader"),
    path("display_meta", display_meta)
]
