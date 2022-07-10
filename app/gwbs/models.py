from django.db import models

from tinymce.models import HTMLField

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    """
    考生信息表
    """
    name = models.CharField(max_length=50, verbose_name="考生姓名")
    candidate_num = models.CharField(max_length=100, unique=True, verbose_name="准考证号")
    password = models.CharField(max_length=256, default="123456", verbose_name="登录密码")
    room = models.ForeignKey('Room', on_delete=models.CASCADE, verbose_name="所在考室")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="修改时间")

    def to_dict(self, ignore_fileds=()):
        attr_dict = {}
        for field in self._meta.fields:
            name = field.attname
            if name not in ignore_fileds:
                attr_dict[name] = getattr(self, name)
        return attr_dict

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "考生管理"
        verbose_name_plural = verbose_name


class Room(models.Model):
    """
    考室表
    """
    room_name = models.CharField(max_length=50, verbose_name="考室名称")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="修改时间")

    def __str__(self):
        return self.room_name

    class Meta:
        verbose_name = "考室管理"
        verbose_name_plural = verbose_name


class UserAnswer(models.Model):
    """
    作答记录表
    """
    user = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name="考生")
    is_check = models.BooleanField(default=False, verbose_name="是否勾选")
    is_begin = models.BooleanField(default=False, verbose_name="是否开始答题")
    is_over = models.BooleanField(default=False, verbose_name="是否结束考试")
    word_name = models.CharField(max_length=500, null=True, blank=True, verbose_name="Word文件名")
    pdf_name = models.CharField(max_length=500, null=True, blank=True, verbose_name="PDF文件名")
    login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="登录IP")
    login_os = models.CharField(max_length=50, null=True, blank=True, verbose_name="登录操作系统")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="修改时间")

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "作答记录"
        verbose_name_plural = verbose_name


class FileInfo(models.Model):
    """
    文件信息表
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="考生")
    file_name = models.CharField(max_length=500, null=True, blank=True, verbose_name="提交文件名")
    file_path = models.CharField(max_length=500, null=True, blank=True, verbose_name="文件路径")
    file_type = models.CharField(max_length=10, null=True, blank=True, verbose_name="文件类型")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="提交时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "文件信息"
        verbose_name_plural = verbose_name


class ExamContent(models.Model):
    """
    试卷内容表
    """
    title = models.CharField(max_length=255, verbose_name="试卷标题")
    content = HTMLField(blank=True, null=True, verbose_name="试题内容")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="修改时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "试卷管理"
        verbose_name_plural = verbose_name


class ExamTime(models.Model):
    """
    考试时间表
    """
    exam = models.OneToOneField('ExamContent', to_field='id', on_delete=models.CASCADE, verbose_name="试卷标题")
    exam_begin_time = models.DateTimeField(null=True, blank=True, verbose_name="开始时间")
    exam_end_time = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="修改时间")

    def __str__(self):
        return self.exam.title

    class Meta:
        verbose_name = "考试时间"
        verbose_name_plural = verbose_name


class PageInfo(models.Model):
    """
    页面信息表
    """
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name="页面标题")
    user_info_content = HTMLField(verbose_name="考生须知")
    page_footer = models.CharField(max_length=255, null=True, blank=True, verbose_name="页脚标题")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="修改时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "页面信息"
        verbose_name_plural = verbose_name
