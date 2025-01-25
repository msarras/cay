from datetime import date
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from tasks.models import PublishTask


class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard.html'

    today = date.today()

    def get(self, request):
        context = {}
        weekly_basket_published_task = PublishTask.objects.filter(
            task__name='manage_weekly_basket',
            valid_until__gte=date.today()
        )
        context['basket_open'] = True if weekly_basket_published_task else False
        return render(request, self.template_name, context)
