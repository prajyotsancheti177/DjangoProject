from django.shortcuts import redirect, render
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from application.models import UploadedFile
from application import models
from .forms import FileUploadForm
from django.db.models import Count

CustomUser = get_user_model()
# Create your views here.
@login_required(login_url='/')
def home(request):
    received_data = request.session.get('data', '')
    return render(request,"index.html",{"fname":received_data})
    # return render(request, "index.html")

    

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
    if(request.user.is_authenticated):
        logout(request)
    if request.method == "POST":
        email = request.POST['email']
        pass1 = request.POST['pass1']
        user = authenticate(username=email, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            request.session['data'] = fname
            return redirect('home')
            # return render(request,"index.html",{"fname":fname})
        else:
            messages.error(request, "Wrong Credentials")
            return redirect("home")
    
    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('signin')

def authors_sellers_page(request):
    CustomUser = get_user_model()
    user_filter = CustomUser.objects.filter(public_visibility=True)
    return render(request, 'authors_sellers.html', {"users" : user_filter})

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            messages.success(request, 'Book uploaded successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Error uploading the book. Please check the form.')
    else:
        form = FileUploadForm()

    return render(request, 'upload_files.html', {'form': form})

@login_required
def uploaded_images(request):
    received_data = request.session.get('data', '')
    user_files = UploadedFile.objects.filter(user = request.user)
    return render(request, 'uploaded_files.html', {'user_files': user_files, 'received_data' : received_data})
