from django.views.generic import TemplateView
from django.conf import settings
from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.http import Http404
from django.http import HttpResponse, HttpResponseNotFound
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail


class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail


def Home(request):
    """View for the Index page of the website"""
    #template_name = "pages/index.html"
    return render(request, "pages/index.html")





class UserFormView(View):
    form_class = UserForm
    template_name = 'pages/registration_form.html'
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            human = True
            user = form.save(commit=False)
            # cleaned()normalized data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #return user objects
            user = authenticate(username=email, password = password)

            if user is not None and user.is_active:
                login(request,user)
                return redirect('/')

        return render(request, self.template_name)

def logout(request):
    auth.logout(request)
    return redirect('/')

class LoginView(View):
    def get(self, request):
        return HttpResponseNotFound('<h1>Page not found</h1>')
    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']

        #return user objects
        user = authenticate(username=username, password = password)


        if user is not None and user.is_active:
            login(request,user)
            return redirect('/accounts/profile/')
        else:
            return render(request, 'pages/unregister_or_unactivation.html')
