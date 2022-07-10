# -*- coding: utf-8 -*-
# @Time    : 09/06/2021 09:58
# @Author  : Spring
# @FileName: upload_answer_file.py
# @Software: PyCharm
import os

from GWWeb import settings
from app.gwbs.tools import RJson


class UploadAnserFile():
    def __init__(self, user, file_obj):
        self.can_num = user.candidate_num
        self.room_id = user.room_id
        self.name = user.name
        self.file_obj = file_obj
        self.path = os.path.join(settings.MEDIA_ROOT, 'upload/0{0}考室/{1}'.format(self.room_id, self.can_num))
        self.create_dir()

    def create_dir(self):
        """
        # 创建上传目录
        :return:
        """

        if os.path.exists(self.path):
            print("目录已经存在")
        else:
            os.makedirs(self.path)
