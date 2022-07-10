from braces import views

# Create your views here.
from django.views.generic.base import View

from pyecharts import options as opts
from pyecharts.charts import Bar
from django.http import HttpResponse

from app.gwbs.models import UserAnswer, User


class UserAnswerShow(views.LoginRequiredMixin, views.PermissionRequiredMixin, View):
    """
    作答记录图
    """
    permission_required = "gwbs.view_user"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        user_all_count = User.objects.all().count()
        user_answer_login_count = UserAnswer.objects.all().count()
        is_over_count = UserAnswer.objects.filter(is_over=1).count()

        c = (
            Bar()
                .add_xaxis(["统计图", ])
                .add_yaxis("所有考生", [user_all_count, ], )
                .add_yaxis("已登录考生", [user_answer_login_count, ])
                .add_yaxis("交卷考生", [is_over_count, ])
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="公文比赛答题情况",
                    pos_left="center",
                    title_textstyle_opts={"font_size": 28, }
                ),
                legend_opts=opts.LegendOpts(pos_bottom=0)
            )
        )
        print(request.user.username[7:])
        print(type(request.user))
        return HttpResponse(c.render_embed())
