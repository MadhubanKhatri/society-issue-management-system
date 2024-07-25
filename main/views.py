from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member, Issue
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password

User = get_user_model()


def home(request):
    if(request.user.is_authenticated):
        return redirect('member_loggedin')        
    elif('admin_user' in request.session):
        return redirect('dashboard')
    else:
        return render(request,'home.html')


def signup(request):    
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        phone = request.POST['phone']
        city = request.POST['city']
        state = request.POST['state']
        address = request.POST['address']
        profession = request.POST['profession']
        maritial_status = request.POST['maritial_status']
        
        if(name!='' or password!='' or phone!='' or city!='' or state!='' or address!=''):
            create_member = User(username=name, password=make_password(password),first_name=name, contact_num=phone, city=city, state=state, 
                                   profession=profession,address=address,marritial_status=maritial_status)
            create_member.save()
            messages.success(request,"Member is created successfully.")
        else:
            messages.warning(request,"Please fill all the fields.")
        return redirect('home')

def custom_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            user_name = request.POST['user_name']
            password = request.POST['password']
            
            check_user = authenticate(username = user_name, password = password)

            if check_user is not None:
                login(request, check_user)
            else:
                messages.warning(request,"Invalid username or password.")
            return redirect('home')
           
    else:
        return redirect('home')


def member_loggedin(request):
    # session_user = request.session['username']
    if request.user.is_authenticated:
        session_user = request.user
        member_data = User.objects.get(username=session_user)
        print(member_data)
        # member_data = Member.objects.get(name=session_user)
        member_issues = Issue.objects.filter(member=member_data)

        return render(request, 'welcome.html', {'session_user': session_user, 'member_data': member_data, 
                                                'member_issues':member_issues})
    else:
        return redirect('home')



def custom_logout(request, flag):
    if(flag=='IsAdmin'):
        if('admin_user' in request.session):
            del request.session['admin_user']
            messages.success(request, 'You are logout successfully.')
        else:
            messages.warning(request, 'You are not logged in.')
    
    if(flag=='IsUser'):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'You are logout successfully.')
        else:
            messages.warning(request, 'You are not logged in.')
    return redirect('home')



def create_issue(request):
    if request.method == 'POST':
        heading = request.POST['heading']
        description = request.POST['description']

        session_user = request.user
        
        create_new_issue = Issue(member=session_user, heading=heading, description=description, wing=session_user.wing, 
                                                flat=session_user.flat,status='Raised', pcd=timezone.now())
        create_new_issue.save()
        messages.success(request, 'New issue is raised.')
    return redirect('home')
    

def dashboard(request):
    if('admin_user' in request.session):
        members_issue_details = Issue.objects.all().order_by('-pcd')
        data = {'member_issues': members_issue_details}
        return render(request, 'dashboard.html', data)
    else:
        return redirect('home')


def admin_panel_login(request):
    if request.method == 'POST':
        admin_username = request.POST['admin_username']
        admin_password = request.POST['admin_password']

        if(admin_username!='' or admin_password!=''):
            check_user = User.objects.get(username=admin_username)
            if check_user and check_password(admin_password, check_user.password):
                request.session['admin_user'] = admin_username
                return redirect('dashboard')
            else:
                messages.warning(request,"Invalid admin username or password.")
            return redirect('home')
        else:
            messages.warning(request,"Please fill all the fields.")
            return redirect('home')
        



def edit_issue(request, issue_id):
    if (request.method == 'POST'):
        prd = request.POST['prd']
        issue_status = request.POST['status']

        raised_issue = Issue.objects.get(id=issue_id)
        raised_issue.prd = prd
        raised_issue.status = issue_status
        raised_issue.save()
    return redirect('home')