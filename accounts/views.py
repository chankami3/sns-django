from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import LoginForm

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
