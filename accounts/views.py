from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        passw = request.POST['password']
        conpassw = request.POST['conpass']

        user = User.objects.create_user(username = username,email=email, password= passw)
        if passw != conpassw:
            print('Passwords don\'t match')
        else:
            user.save()
            return redirect('accounts:login')
    return render(request, 'accounts/signup1.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        passw = request.POST['pass']
        user = auth.authenticate(username = username ,password = passw)

        if user:
            auth.login(request,user)
            return redirect('products:mainpage')
        else:
            return redirect('accounts:login')
    else:
        return render(request,'accounts/signin.html')

def lgout(request):
    logout(request)
    return redirect('products:mainpage')
