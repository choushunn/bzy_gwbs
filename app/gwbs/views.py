# -*- coding: utf-8 -*-
# @Time    : 12/06/2021 10:30
# @Author  : Spring
# @FileName: views.py
# @Software: PyCharm


import os

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from GWWeb import settings
from app.gwbs.forms import UserLoginForm
from app.gwbs.models import User, UserAnswer, FileInfo, ExamContent, PageInfo
# 登录逻辑
from app.gwbs.tools import RJson


def get_page_info(request):
    """

    :param request:
    :return:
    """
    try:
        page_info = PageInfo.objects.first()
    except Exception as e:
        page_info['user_info_content'] = "暂无"

    return page_info


def display_meta(request):
    values = request.META.items()
    # values.sort()
    html = []
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    html.append(ip)
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


class LoginView(View):
    """
    登录视图
    """

    def get(self, request):
        """
        # 显示登录页面
        # 已登录则跳转到info
        :param request:
        :return:
        """

        return render(request, 'login/login.html')

    def post(self, request):
        """
        # 获取登录表单
        # 验证表单数据
        # 写入session
        # 写入数据库
        # 跳转
        :param request:
        :return:
        """

        user_login_form = UserLoginForm(request.POST).clean_data(request)
        if user_login_form:
            try:
                user = User.objects.get(candidate_num=user_login_form['candidate_num'])
            except ObjectDoesNotExist:
                msg = "准考证输入有误！"
                return render(request, 'login/login.html', locals())
            else:
                if user.password == user_login_form['password']:
                    try:
                        user_answer, _ = UserAnswer.objects.update_or_create(user=user, defaults={
                            'login_ip': user_login_form['login_ip'],
                            'login_os': user_login_form['os'],
                        })
                    except Exception as e:
                        msg = "密码不正确！"
                        return render(request, 'login/login.html', locals())
                    else:
                        if user_answer.login_ip and (user_answer.login_ip != user_login_form['login_ip']):
                            msg = "已经在其他电脑上登录！"
                            return render(request, 'login/login.html', locals())
                        request.session['ks_id'] = user.id
                        print(user_answer)
                        return HttpResponseRedirect(reverse("info"))
                else:
                    msg = "密码不正确！"
                    return render(request, 'login/login.html', locals())
        else:
            msg = "准考证输入有误！"
            return render(request, 'login/login.html', locals())


class InfoView(View):
    """
    # 考试须知
    # 显示页面信息
    # 是否登录，跳转
    # 是否勾选，跳转
    # 判断时间，跳转
    """

    def get(self, request):
        """

        :param request:
        :return:
        """
        page_info = get_page_info(request)
        try:
            user = User.objects.get(id=request.session['ks_id'])
            is_check = user.useranswer.is_check
        except Exception as e:
            return HttpResponseRedirect(reverse("login"))
        else:
            if is_check and request.session['count_down'] < 0:
                return HttpResponseRedirect(reverse("index"))
        return render(request, 'gwbs/info.html', locals())

    # 开始考试
    def post(self, request):
        """
        # 判断勾选，并存入
        # 存入开始时间
        :param request:
        :return:
        """

        is_check = request.POST.get("check1")
        if is_check == "on":
            UserAnswer.objects.update_or_create(
                user_id=request.session['ks_id'],
                defaults={
                    "user_id": request.session['ks_id'],
                    "is_check": True,
                    "is_begin": True,
                }
            )
            return HttpResponseRedirect(reverse("index"))
        return render(request, 'gwbs/info.html')


class IndexView(View):
    """
    # 答题界面
    """

    # 页面展示
    def get(self, request):
        """
        # 是否登录，返回到登陆
        # 是否勾选，返回到勾选
        # 获取开考时间
        # 判断时间，没过期传时间，过期跳转到结束
        # 判断上传成功
        :param request:
        :return:
        """
        page_info = get_page_info(request)
        if request.session['count_down'] > 0:
            return HttpResponseRedirect(reverse("info"))

        try:
            user_answer = UserAnswer.objects.get(user_id=request.session['ks_id'])
        except Exception as e:
            word_file_status = "未提交"
            pdf_file_status = "未提交"
        else:
            word_file_status = user_answer.word_name
            pdf_file_status = user_answer.pdf_name
            print(user_answer)
            is_check = user_answer.is_check
            is_over = user_answer.is_over
            if not is_check:
                return HttpResponseRedirect(reverse("info"))
            if is_over:
                return HttpResponseRedirect(reverse("over"))

        try:
            exam_info = ExamContent.objects.first()
        except Exception as e:
            exam_info = "试题还未发布，请等待。"
        else:
            exam_info = exam_info.content

        return render(request, 'gwbs/index.html', locals())

    # 交卷逻辑
    def post(self, request):
        """
        # 设置交卷标志、锁定页面
        # 检查文件是否上传
        :param request:
        :return:
        """

        useranswer = UserAnswer.objects.get(user_id=request.session['ks_id'])
        if useranswer.is_over:
            return RJson(405, "你已交卷，请不要重复提交！", "")

        word_is_up = useranswer.word_name
        pdf_is_up = useranswer.pdf_name

        if not word_is_up:
            return RJson(404, "请上传 WORD 文件！", "")

        if not pdf_is_up:
            return RJson(404, "请上传 PDF 文件！", "")

        useranswer.is_over = True
        useranswer.save()
        return RJson(200, "交卷成功！正在跳转....", "")


class OverView(View):
    """
    结束考试
    """

    def get(self, request):
        """

        :param request:
        :return:
        """
        page_info = get_page_info(request)
        return render(request, 'gwbs/over.html', locals())


class Uploader(View):
    """
    # 文件上传逻辑
    """

    def post(self, request):
        """

        :param request:
        :return:
        """
        # 获取文件对象
        file_obj = request.FILES.get("file1", None)
        # 判断文件是否存在
        if file_obj is None:
            return RJson(404, "请选择文件", "")

        # 获取文件类型
        file_type = file_obj.name.split('.')[1]

        # 转换为小写
        file_type = file_type.lower()

        # 判断文件类型是否合法
        if file_type not in ['doc', 'docx', 'pdf']:
            return RJson(305, "请选择正确的文件类型！", "")
        # 获取交卷状态
        user = User.objects.get(id=request.session['ks_id'])
        if user.useranswer.is_over:
            return RJson(405, "你已交卷，请不要重复提交！", "")

        # 获取考室
        can_num = user.candidate_num
        # 创建上传目录
        path = os.path.join(settings.MEDIA_ROOT, 'upload/0{0}考室/{1}'.format(user.room_id, can_num))
        if os.path.exists(path):
            print("目录已经存在")
        else:
            os.makedirs(path)
        file_name = None
        if file_type == "pdf":
            # 如果pdf文件存在
            if user.useranswer.pdf_name:
                exists_file = os.path.join(path, user.useranswer.pdf_name)
                if os.path.exists(exists_file):
                    os.remove(exists_file)
            file_name = '{0}_{1}.{2}'.format(can_num, user.name, file_type)
            UserAnswer.objects.filter(user_id=request.session['ks_id']).update(
                pdf_name=file_name)
        elif file_type in ["docx", "doc"]:
            if user.useranswer.word_name:
                exists_file = os.path.join(path, user.useranswer.word_name)
                if os.path.exists(exists_file):
                    os.remove(exists_file)

            file_name = '{0}_{1}.{2}'.format(can_num, user.name, file_type)
            UserAnswer.objects.filter(user_id=request.session['ks_id']).update(
                word_name=file_name)

        file_path = os.path.join(path, file_name)
        print(file_path)
        # 写入文件
        f = open(file_path, 'wb+')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()

        # 保存上传文件记录
        FileInfo.objects.create(
            user_id=request.session['ks_id'],
            file_name=file_name,
            file_path=file_obj.name,
            file_type=file_type
        )
        return RJson(200, "上传成功！", "")
