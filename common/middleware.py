# -*- coding: utf-8 -*-
# @Time    : 12/06/2021 10:30
# @Author  : Spring
# @FileName: middleware.py
# @Software: PyCharm
import datetime
import time

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from app.gwbs.models import User, ExamTime, UserAnswer
from common import errors
from lib.http import render_json


class AuthMiddleware(MiddlewareMixin):
    white_list = [
        "/info",
        "/gwbs",
        "/over"
    ]

    def process_request(self, request):
        """
        用户登录验证
        :param request:
        :return:
        """
        # 检查当前path是否在白名单内
        if request.path not in self.white_list:
            return

        # 用户身份验证
        uid = request.session.get('ks_id')
        if uid is None:
            # 拦截并返回信息
            # return render_json(None, errors.LOGIN_REQUIRE)
            return HttpResponseRedirect(reverse("login"))
        else:
            try:
                user = User.objects.get(id=uid)
            except User.DoesNotExist:
                # 不存在
                # return render_json(None, errors.USER_NOT_EXIST)
                return HttpResponseRedirect(reverse("login"))
            else:
                pass
        if request.path == '/gwbs':
            try:
                user_answer = UserAnswer.objects.get(user_id=request.session['ks_id'])
            except Exception as e:
                return HttpResponseRedirect(reverse("login"))
            else:
                if user_answer.is_over:
                    return HttpResponseRedirect(reverse("over"))
                if not user_answer.is_check:
                    return HttpResponseRedirect(reverse("info"))


class ExamTimeMiddleware(MiddlewareMixin):
    white_list = [
        "/info",
        "/over",
        "/gwbs",
    ]
    remain_time = 0
    count_down = 0

    def process_request(self, request):
        """
        用户登录验证
        :param request:
        :return:
        """
        # 检查当前path是否在白名单内
        if request.path in self.white_list:
            try:
                exam_time = ExamTime.objects.first()
            except Exception as e:
                print(e)
                return HttpResponseRedirect(reverse("login"))
            else:
                start_timestamp = time.mktime(exam_time.exam_begin_time.timetuple())
                end_timestamp = time.mktime(exam_time.exam_end_time.timetuple())
                cur_timestamp = time.mktime(datetime.datetime.now().timetuple())

                self.remain_time = end_timestamp - cur_timestamp
                print("结束考试剩余时间", self.remain_time)
                self.count_down = start_timestamp - cur_timestamp
                request.session['remain_time'] = self.remain_time
                request.session['count_down'] = self.count_down
                if request.path == '/gwbs':
                    if self.remain_time < 0:
                        return HttpResponseRedirect(reverse("over"))
                print("开始考试倒计时", self.count_down)
