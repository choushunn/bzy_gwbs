from django.contrib import admin
from django.contrib import messages
# Register your models here.


from app.gwbs.models import User, UserAnswer, ExamTime, FileInfo, ExamContent, Room, PageInfo

from import_export.admin import ImportExportModelAdmin as IEModuleAdmin
from import_export.admin import ExportMixin

from lib.zipstream import export_answer_zip
from guardian.admin import GuardedModelAdmin

# 修改网页title和站点header。
admin.site.site_title = "公文竞赛管理系统"
admin.site.site_header = "公文竞赛管理系统"


@admin.register(User)
class UserAdmin(IEModuleAdmin, GuardedModelAdmin):
    """
    考生管理
    """
    list_display = (
        'id', 'name', 'candidate_num', 'room', 'password', 'create_time', 'update_time')
    list_display_links = ('name',)
    autocomplete_fields = ['room', ]
    list_filter = ('room',)
    search_fields = ('name',)
    ordering = ('id',)

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.username[:7] == "jiankao":
            return qs.filter(room_id=int(request.user.username[7:]))
        return qs.none()


class UserInline(admin.TabularInline):
    """
    考生内联
    """
    extra = 0
    readonly_fields = ['id', 'name', 'candidate_num', 'room', 'password', 'create_time', 'update_time']
    verbose_name = "考生"
    can_delete = False
    model = User
    verbose_name_plural = verbose_name

    def has_add_permission(self, request, obj=None):
        """ 不允许这个inline类增加记录 (当然也增加不了，readonly_fileds中定义的字段，在增加时无法输入内容) """
        return False


@admin.register(Room)
class RoomAdmin(IEModuleAdmin, GuardedModelAdmin):
    """
    考室管理
    """
    list_display = (
        'id', 'room_name', 'create_time', 'update_time')
    list_display_links = ('room_name',)
    list_filter = ('room_name',)
    ordering = ('id',)
    inlines = [UserInline, ]
    search_fields = ('room_name',)


@admin.register(UserAnswer)
class UserAnswerAdmin(ExportMixin, GuardedModelAdmin):
    """
    考生作答记录管理
    """
    list_display = (
        'id', 'user', 'is_check', 'is_begin', 'is_over', 'login_ip', 'login_os', 'word_name', 'pdf_name', 'create_time',
        'update_time')
    readonly_fields = ('word_name', 'pdf_name', 'login_ip', 'login_os',)
    list_display_links = ('user',)
    list_filter = ('is_check', 'is_begin', 'is_over',)
    date_hierarchy = 'create_time'
    search_fields = ('user',)
    ordering = ('id',)
    actions = ['reset_is_over', 'reset_login_ip', 'export_file']

    def get_queryset(self, request):
        qs = super(UserAnswerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.username[:7] == "jiankao":
            return qs.filter(user__room_id=int(request.user.username[7:]))
        return qs.none()

    @admin.display(
        boolean=True,
        ordering='-login_ip',
        description='重置登录',
    )
    @admin.action(
        permissions=['change'],
        description='Mark selected stories as change',
    )
    def reset_login_ip(self, request, queryset):
        """
        重置登录IP
        :param request:
        :param queryset:
        :return:
        """
        queryset.update(login_ip=None)
        messages.add_message(request, messages.SUCCESS, '重置登录IP成功')

    reset_login_ip.type = 'danger'
    reset_login_ip.confirm = '是否重置登录？'

    @admin.display(
        boolean=True,
        ordering='-login_ip',
        description='撤销交卷',
    )
    @admin.action(
        permissions=['change'],
        description='Mark selected stories as change',
    )
    def reset_is_over(self, request, queryset):
        """
        撤销交卷
        :param request:
        :param queryset:
        :return:
        """
        queryset.update(is_over=0)
        messages.add_message(request, messages.SUCCESS, '撤销交卷成功')

    reset_is_over.type = 'danger'
    reset_is_over.confirm = '是否撤销交卷？'

    @admin.display(
        boolean=True,
        ordering='-id',
        description='导出文件',
    )
    @admin.action(
        permissions=['change', ],
        description='Mark selected stories as change',
    )
    def export_file(self, request, queryset):
        """
        导出答题包按钮
        :param request:
        :param queryset:
        :return:
        """
        path = "./media/upload/"
        try:
            answer_zip = export_answer_zip(path)
            if answer_zip:
                messages.add_message(request, messages.SUCCESS, '导出答题文件成功')
                return answer_zip
            messages.add_message(request, messages.ERROR, '导出答题文件失败')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, '导出答题文件失败')

    export_file.type = 'danger'
    export_file.confirm = '是否导出所有答题文件？'


@admin.register(FileInfo)
class FileInfoAdmin(ExportMixin, GuardedModelAdmin):
    """
    考生上传文件管理
    """
    list_display = ('id', 'user', 'file_name', 'file_path', 'file_type', 'create_time', 'update_time')
    readonly_fields = ('file_name', 'file_path', 'file_type')
    list_display_links = ('user',)
    list_filter = ('file_type',)
    search_fields = ('user',)
    ordering = ('id',)


class ExamTimeInline(admin.StackedInline):
    """
    # TabularInline
    """
    extra = 0
    model = ExamTime


@admin.register(ExamContent)
class ExamContentAdmin(IEModuleAdmin, GuardedModelAdmin):
    """
    试卷内容管理
    """
    list_display = ('id', 'title', 'create_time', 'update_time')
    list_display_links = ('title',)
    search_fields = ('title',)
    ordering = ('id',)
    inlines = [ExamTimeInline, ]


@admin.register(PageInfo)
class PageInfoAdmin(GuardedModelAdmin):
    list_display = ('id', 'title', 'create_time', 'update_time')
    list_display_links = ('title',)
