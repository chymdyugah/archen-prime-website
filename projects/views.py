from typing import Any
from django.forms import BaseModelForm
from django.views.generic import TemplateView, DetailView, ListView, View, CreateView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView as LV

from projects.forms import UploadFileForm
from .models import Images, Project
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect, render


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwaags):
        project_count = Project.objects.count()
        return render(request, self.template_name, {'project_count': project_count})


class ProjectsView(ListView):
    model = Project
    context_object_name = 'projects'
    paginate_by = 9
    template_name = 'projects.html'
    
    def get(self, request, *args, **kwargs):
        try:
            details = {
                'real-estate': {
                    'details': 'At Archen Prime Limited, our real estate services are all about creating vibrant and sustainable communities. Whether you’re looking to develop a new property, manage an existing one, or invest in real estate, we’re here to guide you every step of the way. Our dedicated team is passionate about transforming spaces into thriving environments where people can live, work, and thrive. We take pride in offering innovative solutions that meet the highest standards of quality and sustainability.',
                    'icon': 'ri-community-line',
                    'image': 'img-1.jpg',
                },
                'consultancy': {
                    'details': 'At Archen Prime Limited, we believe that great design makes life better. Our design and consultancy services cover everything from architectural and interior design to comprehensive project management. We work closely with you to understand your needs and preferences, creating spaces that are not only stunning but also functional and eco-friendly. Our creative designers and experienced consultants are dedicated to bringing your vision to life, ensuring that every detail is just right.',
                    'icon': 'ri-user-2-line',
                    'image': 'consultancy-1.jpg',
                },
                'construction': {
                    'details': 'Building dreams is at the heart of what we do at Archen Prime Limited. From constructing new homes and commercial spaces to renovating and remodeling existing ones, we bring precision and excellence to every project. Our experienced professionals use the latest techniques and materials to create structures that are not only beautiful but also built to last. We focus on sustainability and durability, ensuring that each project stands the test of time while reflecting your unique vision.',
                    'icon': 'ri-hammer-line',
                    'image': 'construction-1.jpg',
                }
            }
            tag:str = kwargs['tag']
            self.object_list = self.get_queryset().filter(tags__icontains=tag)
            context = self.get_context_data()
            context['tag'] = tag.replace('-', ' ').capitalize()
            context['page_details'] = details[tag]
            print(context)
            return self.render_to_response(context)
        except:
            return HttpResponseRedirect(reverse('home'))


class ViewProjectView(DetailView):
    model = Project
    slug_field = 'project_key'
    slug_url_kwarg = 'key'
    context_object_name = 'project'
    template_name = 'project-gallery.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['images'] = project.images_set.all()
        return context


class LoginView(LV):
    template_name = 'custom-admin/login.html'

    def post(self, request, *args, **kwargs):
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user.last_login = timezone.now()
                user.save()
                if request.GET.get('next') is not None:
                    return HttpResponseRedirect(request.GET['next'])
                
                return HttpResponseRedirect(reverse('all_projects'))
            else:
                messages.error(request, "Invalid Login")
        
        else:
            messages.error(request, "Invalid Login")
        
        return self.get(request, *args, **kwargs)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


@method_decorator(login_required, 'dispatch')
class AddProjectView(CreateView):
    template_name = 'custom-admin/add-project.html'
    model = Project
    fields = ['name', 'cover_image', 'tags', 'project_date', 'client', 'description']
    success_url = '/all-projects/'


@method_decorator(login_required, 'dispatch')
class AllProjectsView(ListView):
    template_name = 'custom-admin/search.html'
    model = Project
    context_object_name = 'projects'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        
        term = request.GET.get('term')
        if term is not None:
            results = self.object_list.filter(
                Q(name__icontains=term) | 
                Q(client__icontains=term) | 
                Q(tags__icontains=term)
            )
            context = self.get_context_data()
            context['projects'] = results
            
            return self.render_to_response(context)
        return self.render_to_response(context)


@method_decorator(login_required, 'dispatch')
class EditProjectView(UpdateView):
    model = Project
    slug_field = 'project_key'
    slug_url_kwarg = 'key'
    context_object_name = 'project'
    template_name = 'custom-admin/edit-project.html'
    fields = ['name', 'cover_image', 'description', 'tags', 'client', 'project_date']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['images'] = project.images_set.all()
        return context
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print(self.request.POST)
        tags = self.request.POST.getlist('tags')
        tags = ", ".join(tags)
        form.instance.tags = tags
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        obj = self.get_object()
        return f'/edit-project/{obj.project_key}'


@method_decorator(login_required, 'dispatch')
class AddImageView(CreateView):
    model = Images
    fields = ('image',)

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(project_key=kwargs['key'])
        for f in request.FILES.getlist('image'):
            form = UploadFileForm({'project': project}, {'image': f})
            print(form)
            if form.is_valid():
                # file is saved
                form.save()
        return HttpResponseRedirect(reverse('edit_project', kwargs={'key': project.project_key}))


@method_decorator(login_required, 'dispatch')
class DeleteImageView(DeleteView):
    model = Images
    success_url = '/all-projects/'


@method_decorator(login_required, 'dispatch')
class DeleteProjectView(DeleteView):
    model = Project
    slug_field = 'project_key'
    slug_url_kwarg = 'key'
    success_url = '/all-projects/'


def page404(request, exception=None):
    return HttpResponseRedirect(reverse('home'))

def page500(request, exception=None):
    return HttpResponseRedirect(reverse('home'))
