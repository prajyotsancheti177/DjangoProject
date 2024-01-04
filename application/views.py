from django.shortcuts import redirect, render
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import CustomUser

# Create your views here.
def home(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        public_visibility = request.POST.get('public_visibility')
        if pass1 != pass2 :
            return HttpResponse("Password and confirm password are diffrent")
        else:
            if public_visibility == 'on':
                public_visibility = True
            else:
                public_visibility = False
        CustomUser = get_user_model()
        myuser = CustomUser.objects.create_user(email, username, pass1)
        myuser.first_name = fname
        myuser.last_name = lname 
        myuser.public_visibility = public_visibility
        myuser.save()  

        # messages.success(request, "Your Account has been successfully created.")     
        return redirect("signin")
    
    return render(request, "signup.html")

def signin(request):
    if request.method == "POST":
        email = request.POST['emial']
        pass1 = request.POST['pass1']
        user = authenticate(username=email, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request,"index.html",{"fname":fname})
        else:
            messages.error(request, "Wrong Credentials")
            return redirect("home")
    
    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('home')

def user_list(request):
    users= CustomUser.objects.all()
    # print(users)
    return render (request, "userlist.html",{"users":users})

# def register(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         username = request.POST['username']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']
#         name = request.POST['name']
#         city = request.POST['city']
#         state = request.POST['state']
#         card_no = request.POST['card_no']
#         print("I am here")
#         myuser = User.objects.create_user(email, username, pass1)
#         # myuser.first_name = fname
#         # myuser.last_name = lname 
#         myuser.save()  

#         # messages.success(request, "Your Account has been successfully created.")     
#         return redirect("login")

#     return render(request,'register.html')

# def login_user(request):
#     return render(request,'login.html')
