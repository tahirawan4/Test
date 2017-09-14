# class EventPassCreateView(DashboardAccessMixin, DashboardMixin, TemplateView):
#     template_name = "dashboard/events/event_pass_create.html"
#
#     def get_queryset(self):
#         return EventPass.objects.all()
#
#     def check_permissions(self, request, *args, **kwargs):
#         org_id = kwargs.get('org_id')
#         has_access = False
#         if org_id is not None:
#             has_access = OrganizationUser.objects.filter(
#                 organization=org_id,
#                 user=request.user
#             ).exists()
#         return has_access
#
#     def get_context_data(self, **kwargs):
#         context = super(EventPassCreateView, self).get_context_data(**kwargs)
#         return context
#
#     def get(self, request, **kwargs):
#         context = super(EventPassCreateView, self).get_context_data(**kwargs)
#         selected_org = self.get_selected_org()
#         form_class = EventPassCreateForm(selected_org.site.all())
#         context['form'] = form_class
#         return render(request, self.template_name, context)
#
#     def post(self, request, **kwargs):
#         form = EventPassCreateForm(None, request.POST)
#         context = super(EventPassCreateView, self).get_context_data(**kwargs)
#         if form.is_valid():
#             form.save()  # let move to the selection of question groups
#             return redirect(reverse("dashboard:event_pass_list", args=[self.get_selected_org().id]))
#         context['form'] = form
#         return render(request, self.template_name, context)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from animals.forms import DogForm, CatForm
from animals.models import Dog, Cat


class DogCreate(CreateView):
    form_class = DogForm
    template_name = 'create.html'
    success_url = '/index/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(DogCreate, self).form_valid(form)


class DogUpdate(UpdateView):
    template_name = 'create.html'
    model = Dog
    fields = ['name', 'birthday']
    success_url = '/index/'


class CatCreate(CreateView):
    form_class = CatForm
    template_name = 'create.html'
    success_url = '/index/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CatCreate, self).form_valid(form)


class CatUpdate(UpdateView):
    template_name = 'create.html'
    model = Cat
    fields = ['name', 'birthday']
    success_url = '/index/'


@login_required(login_url='/login/')
def animals_list(request):
    user = request.user
    cats = Cat.objects.filter(owner=user)
    dogs = Dog.objects.filter(owner=user)

    return render_to_response('index.html', {'dogs': dogs, 'cats': cats})
