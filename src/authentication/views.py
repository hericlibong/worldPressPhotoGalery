from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View

from . import forms


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user =form.save()
            #auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context = {'form':form}) 


def logout_user(request):
    logout(request)
    return redirect('home')


# class LoginPage(View):
#     form_class = forms.LoginForm
#     template_name = 'authentication/login.html'

#     def get(self, request):
#         form = self.form_class()
#         message = ''
#         return render(
#             request, self.template_name, 
#             context={'form':form, 'message':message}
#             )
    
#     def post(self, request):
#         form = self.form_class(request.POST)
#         message = ''
#         if form.is_valid():
#             user = authenticate(
#                 username = form.cleaned_data['username'],
#                 password = form.cleaned_data['password'],
#             )
#             if user is not None:
#                 login(request, user)
#                 return redirect('date_list')
#             else:    
#                 message = 'User or Password invalids'
#         return render(
#             request, self.template_name, 
#             context={'form':form, 'message':message}
#             )







# def login_page(request):
#     form = forms.LoginForm()
#     message = ''
#     if request.method == 'POST':
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 username = form.cleaned_data['username'],
#                 password = form.cleaned_data['password'],
#             )
#             if user is not None:
#                 login(request, user)
#                 return redirect('date_list')    
#         message = 'User or Password invalids'
#     return render(request, 'authentication/login.html', context={'form':form, 'message':message})


# def logout_user(request):
#     logout(request)
#     return redirect('date_list')