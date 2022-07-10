# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 15:06
# @Author  : Spring
# @FileName: forms.py
# @Software: PyCharm
from django import forms

from app.gwbs.models import User


class UserLoginForm(forms.Form):
    """
     考生登录验证
    """
    candidate_num = forms.CharField(label="准考证号", required=True, min_length=3, max_length=20)
    password = forms.CharField(label="密码", required=True)

    def clean_data(self, request):
        """
        清洗表单数据
        :param request:
        :return:
        """
        if self.is_valid():
            self.cleaned_data['login_ip'] = request.META.get("REMOTE_ADDR")
            self.cleaned_data['os'] = request.META.get("OS")
            return self.clean()
        else:
            return self.errors()