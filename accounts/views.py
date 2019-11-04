from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm

from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.mail import EmailMessage
from django.conf import settings


class UserCreateView(FormView):
    form_class = UserCreationForm
    template_name = 'accounts/create.html'
    success_url = reverse_lazy('sns:index')

    def form_valid(self, form):
        if self.request.POST['next'] == 'confirm':
            return render(self.request, 'accounts/create_confirm.html', {'form':form})
        elif self.request.POST['next'] == 'regist':
            form.save()
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            login(self.request, user)
            return super().form_valid(form)
        else:
            print('error...')
            return redirect(reverse_lazy('sns:index'))


class Login(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            subject = 'login'
            message = 'loginしました'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = ['hoge@gmail.com']
            email = EmailMessage(subject, message, from_email, recipient_list)
            email.send()
            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Logout(LogoutView, LoginRequiredMixin):
    template_name = 'accounts/logout.html'