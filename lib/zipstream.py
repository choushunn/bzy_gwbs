# -*- coding: utf-8 -*-
# @Time    : 08/06/2021 21:04
# @Author  : Spring
# @FileName: zipstream.py
# @Software: PyCharm
import time
import os

from django.http import StreamingHttpResponse

import zipstream


class ZipUtilities:
    zip_file = None

    def __init__(self):
        self.zip_file = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)

    def toZip(self, file, name):
        if os.path.isfile(file):
            self.zip_file.write(file, arcname=os.path.basename(file))
        else:
            self.addFolderToZip(file, name)

    def addFolderToZip(self, folder, name):
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                self.zip_file.write(full_path, arcname=os.path.join(name, os.path.basename(full_path)))
            elif os.path.isdir(full_path):
                self.addFolderToZip(full_path, os.path.join(name, os.path.basename(full_path)))

    def close(self):
        if self.zip_file:
            self.zip_file.close()


def export_answer_zip(path):
    """
    导出作答文件
    :param path:
    :return:
    """
    zip_util = ZipUtilities()
    file_date = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    file_name = "answer-" + file_date
    zip_util.addFolderToZip(path, file_name)
    response = StreamingHttpResponse(zip_util.zip_file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name + ".zip")
    return response
