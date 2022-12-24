from django.contrib.auth.models import User
from django.forms.models import BaseModelForm
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class HelpView(TemplateView):
    template_name = 'help.html'


class SignUpView(CreateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password']
    template_name = 'signup.html'
    success_url = '/'
    success_message = 'Account created successfully!'
    error_message = 'Account creation failed!'

    def form_valid(self, form: BaseModelForm):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        return super(SignUpView, self).form_valid(form)

    def get(self, request: HttpRequest, *args: str, **kwargs: str):
        if request.user.is_authenticated:
            return redirect('/')

        return super(SignUpView, self).get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: str):
        if request.user.is_authenticated:
            return redirect('/')

        return super(SignUpView, self).post(request, *args, **kwargs)


class UserDetailView(DetailView):
    model = User

    def get(self, request: HttpRequest, *args: str, **kwargs: str):
        user = get_object_or_404(User, username=kwargs.get('pk'))

        return render(request, template_name='profile.html', context={'user': user})
