from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
# from application.models import UploadedFile
from application.models import UploadedFile, departmentData, employeeData
from application import models
from .forms import FileUploadForm
import pandas as pd
from django.db.models import Count

CustomUser = get_user_model()
# Create your views here.
@login_required(login_url='/')
def home(request):
    received_data = request.session.get('data', '')
    return render(request,"index.html",{"fname":received_data})
    # return render(request, "index.html")

    

def signup(request):
    print(request.method)
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        public_visibility = request.POST.get('public_visibility')
        if pass1 != pass2:
            return JsonResponse({'error': 'Password and confirm password are different'})
        if public_visibility == 'on':
            public_visibility = True
        else:
            public_visibility = False        

        CustomUser = get_user_model()
        myuser = CustomUser.objects.create_user(email, username, pass1)
        myuser.first_name = fname
        myuser.last_name = lname 
        myuser.public_visibility = public_visibility == 'true'
        myuser.save()
        return JsonResponse({'message': 'User registered successfully!', 'redirect': '/'})

    # return JsonResponse({'error': 'Invalid request'})
        # messages.success(request, "Your Account has been successfully created.")     
        # return redirect("signin")
    
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
            # return redirect("home")
    
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

@login_required
def upload_data(request):
    if request.method == "POST":
        choice = request.POST.get('Upload')
        data = request.FILES.get('upload_file')
        if(data):
            try:
                df = pd.read_excel(data)
                print(df)
                if choice == "Department Data":
                    departmentData.objects.all().delete()
                    unique_departments = df['name'].unique()
                    # deparment_headings = df[['name','description']]
                    # departmentData.objects.bulk_create([departmentData(**row) for row in deparment_headings.to_dict(orient='records')])
                    for department_name in unique_departments:
                        department_instance, created = departmentData.objects.get_or_create(name=department_name, description=f'Description for {department_name}')
                        # print(department_instance)
                elif choice == "Employee Data":
                    employee_data = df[['first_name', 'last_name', 'email', 'year_joined', 'department']]
                    employeeData.objects.all().delete()

                    for _, row in employee_data.iterrows():
                        department_name = row['department']                        
                        # Retrieve the corresponding department instance based on the name
                        department_instance = departmentData.objects.get(name=department_name)
                    # employee_headings = df[['first_name','last_name','email','year_joined','department']]
                    # employeeData.objects.bulk_create([employeeData(**row) for row in employee_headings.to_dict(orient='records')])
                        new_employee = employeeData(
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            email=row['email'],
                            year_joined=row['year_joined'],
                            department=department_instance
                        )
                        new_employee.save()
# annot



                    # employee_headings = df[['first_name','last_name','email','year_joined','department']]
                    # print(employee_headings)
                    # employeeData.objects.all().delete()
                    # employeeData.objects.bulk_create([employeeData(**row) for row in employee_headings.to_dict(orient='records')])
                    # employee_data = [
                    #     {'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com', 'year_joined': 2022, 'department': it_department_instance},
                    # ]
            except pd.errors.ParserError:
                print("Error")
    return render(request,'upload_data.html')