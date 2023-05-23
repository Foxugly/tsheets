from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from weeks.models import WeekDate


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


class GenericCreateView(SuccessMessageMixin, CreateView):
    model = None
    app_name = None
    model_name = None
    fields = "__all__"
    template_name = 'generic_update.html'
    success_url = None
    success_message = _('object created.')
    list_access = set()

    def __init__(self, *args, **kwargs):
        if self.model:
            self.app_name = self.model._meta.app_label
            self.model_name = self.model._meta.model_name
            self.success_url = reverse_lazy('%s:%s_list' % (self.app_name, self.model_name))
        super(GenericCreateView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GenericCreateView, self).get_context_data(**kwargs)
        context['model'] = self.model
        context["title"] = _("Create a new") + " %s" % self.model._meta.verbose_name
        return context

    def dispatch(self, request, *args, **kwargs, ):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.request.user.is_superuser or self.request.user in self.list_access:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class GenericListView(ListView):
    model = None
    paginate_by = 10
    ordering = ['pk']
    template_name = 'generic_list.html'
    team = None
    list_access = set()

    def __init__(self, *args, **kwargs):
        super(GenericListView, self).__init__(*args, **kwargs)

    def setup(self, request, *args, **kwargs):
        super(GenericListView, self).setup(request, *args, **kwargs)
        self.team = self.request.user.get_current_team()

    def get_context_data(self, **kwargs):
        context = super(GenericListView, self).get_context_data(**kwargs)
        context['model'] = self.model
        context["title"] = _("List of ") + "%s" % self.model._meta.verbose_name_plural

        context["team"] = self.team
        context["role"] = self.team.get_role(self.request.user)
        if self.team.is_teamleader(self.request.user):
            context["members"] = self.team.get_all_members()
            context['weeks'] = WeekDate.objects.all().order_by('-start_date')

        return context

    def dispatch(self, request, *args, **kwargs, ):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.request.user.is_superuser or self.request.user in self.list_access:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class GenericUpdateView(SuccessMessageMixin, UpdateView):
    model = None
    app_name = None
    model_name = None
    fields = '__all__'
    template_name = 'generic_update.html'
    success_url = None
    success_message = _('object updated.')
    list_access = set()

    def __init__(self, *args, **kwargs):
        self.team = None
        if self.model:
            self.app_name = self.model._meta.app_label
            self.model_name = self.model._meta.model_name
            self.success_url = reverse_lazy('%s:%s_list' % (self.app_name, self.model_name))
        super(GenericUpdateView, self).__init__(*args, **kwargs)

    def setup(self, request, *args, **kwargs):
        super(GenericUpdateView, self).setup(request, *args, **kwargs)
        self.team = self.request.user.get_current_team()

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs['pk'])
        # return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(GenericUpdateView, self).get_context_data(**kwargs)
        context['model'] = self.model
        context["title"] = _("Edit ") + "%s : %s" % (self.model._meta.verbose_name, self.object)

        context["team"] = self.team
        context["role"] = self.team.get_role(self.request.user)
        if self.team.is_teamleader(self.request.user):
            context["members"] = self.team.get_all_members()
            context['weeks'] = WeekDate.objects.all().order_by('-start_date')

        return context

    def dispatch(self, request, *args, **kwargs, ):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.request.user.is_superuser or self.request.user in self.list_access:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class GenericDetailView(DetailView):
    model = None
    app_name = None
    model_name = None
    template_name = 'generic_detail.html'
    success_url = None
    list_access = set()

    def __init__(self, *args, **kwargs):
        if self.model:
            self.app_name = self.model._meta.app_label
            self.model_name = self.model._meta.model_name
            self.success_url = reverse_lazy('%s:%s_list' % (self.app_name, self.model_name))
        super(GenericDetailView, self).__init__(*args, **kwargs)

    def setup(self, request, *args, **kwargs):
        super(GenericDetailView, self).setup(request, *args, **kwargs)
        self.team = self.request.user.get_current_team()

    def get_context_data(self, **kwargs):
        context = super(GenericDetailView, self).get_context_data(**kwargs)
        context['model'] = self.model
        context["title"] = "%s : %s" % (str(self.model._meta.verbose_name).capitalize(), self.object)

        context["team"] = self.team
        context["role"] = self.team.get_role(self.request.user)
        if self.team.is_teamleader(self.request.user):
            context["members"] = self.team.get_all_members()
            context['weeks'] = WeekDate.objects.all().order_by('-start_date')

        return context

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return self.success_url

    def dispatch(self, request, *args, **kwargs, ):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.request.user.is_superuser or self.request.user in self.list_access:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class GenericDeleteView(SuccessMessageMixin, DeleteView):
    model = None
    app_name = None
    model_name = None
    success_message = _('object deleted.')
    template_name = 'generic_delete.html'
    success_url = None
    list_access = set()

    def __init__(self, *args, **kwargs):
        if self.model:
            self.app_name = self.model._meta.app_label
            self.model_name = self.model._meta.model_name
            self.success_url = reverse_lazy('%s:%s_list' % (self.app_name, self.model_name))
        super(GenericDeleteView, self).__init__(*args, **kwargs)

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(GenericDeleteView, self).get_context_data(**kwargs)
        context['model'] = self.model
        context["title"] = _("Delete ") + " %s : %s" % (self.model._meta.verbose_name, self.object)
        return context

    def get_success_url(self):
        if "next" in self.request.GET:
            return self.request.GET["next"]
        else:
            return self.success_url

    def dispatch(self, request, *args, **kwargs, ):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.request.user.is_superuser or self.request.user in self.list_access:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()
