from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def services(request):
    return render(request,'services.html')

def contact(request):
    return render(request,'contact.html')
def loginn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('Login successful')
        else:
            messages.error(request, 'Invalid username or password')  # Add an error message
            return redirect('login')  # Redirect back to the login page

    return render(request, 'login.html')
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        myuser = User.objects.create_user(username,email,password)
        myuser.save()
        return redirect('login')
    return render(request,'signup.html')

def appoinment(request):
    return render(request,'appoinment.html')