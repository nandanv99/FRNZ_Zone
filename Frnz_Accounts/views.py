from cmath import rect
from ctypes import sizeof
import email
from itertools import count
import re
from tkinter import E
from traceback import print_tb
from urllib.request import HTTPRedirectHandler
from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .models import Friend_request, Interset, user_profile
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user1=user_profile.getUserProfileByUserId(request.user)
        param={'data':user1}
        return render(request,"index.html",param)
    else:
        return render(request,"index.html")

@login_required(login_url='/login')
def chat(request):
    user1=user_profile.getUserProfileByUserId(request.user)
    total_friends=user1.friends.all()
    print(total_friends)
    param={'all_friends':total_friends}
    return render(request,"chats/chat.html",param)

@login_required(login_url='/login')
def chat_duo(request):
    user1=user_profile.getUserProfileByUserId(request.user)
    total_friends=user1.friends.all()
    print(total_friends)
    param={'all_friends':total_friends}
    return render(request,"chats/chat2.html",param)

def register(request):
    return render(request,"accounts/register1.html")

def login_page(request):
    return render(request,"accounts/signin.html")

def handleSignup(request):

        if request.method == 'POST':
            myfile = request.FILES['image']
            username = request.POST['Username']
            firstname = request.POST['Firstname']
            lastname = request.POST['Lastname']
            email = request.POST['Email']
            password = request.POST['Password']
            
            try :
                user = User.objects.create_user(username=username,email=email,password=password)
                user.first_name = firstname
                user.last_name = lastname
                if user is not None:
                    userProfile = user_profile(user = user,fullname = firstname+" "+lastname,image=myfile)
                    userProfile.save()
                    user.save()
                    return redirect("/")
                else:
                    return HttpResponse("user not created")
            except:
                return HttpResponse("Registration failed")
        return HttpResponse("Something went wrong")


def handlesignin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        user = authenticate(request, username = request.POST.get('username'), password = request.POST.get('password'))
        if user is not None :
            login(request, user)
            print(user)
            return redirect('/')
        else:
            return HttpResponse("Something went wrong")

def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login')
def edit_profile(request):
    # Fetching authenticated user1 
    user1=user_profile.getUserProfileByUserId(request.user)
    get_user=User.objects.get(username__contains=request.user)
    # print(user1.image)
    # print(user1.user.email)

    # Total friends objects ( wheter True or False )
    friend_req=Friend_request.getReceiverFriendRequest(user1)

    # For total friends ( Accepted )
    total_friends=user1.friends.all()
    # print(total_friends)

    intrests=Interset.objects.all()
    # print(intrests)

    # For total friend request pending ( Currently false )
    friendlist=[]
    for i in friend_req:
        if(i.status==False):
            friendlist.append(i)

    # print(friendlist[0].sender_user.image)

    param={ 'data':user1,
            'user':get_user,
            'friendscount':len(friendlist),
            'friends_req':friendlist,
            'total_friends':len(total_friends)}

    return render(request,"user_personal/edit_profile.html",param)

@login_required(login_url='/login')
def acceptreq(request,senderid):
    receiveruser=user_profile.getUserProfileByUserId(request.user)
    senderuser=user_profile.getUserProfileById(senderid)
    receiveruser.friends.add(senderuser)
    friendreq=Friend_request.getReceiverFriendRequest(receiveruser)
    print(friendreq)
    for friend in friendreq:
        if friend.sender_user == senderuser:
            # print(friend.sender_user)
            friend.status=True
            # friend.delete()
            friend.save()
    return redirect('/editprofile')

@login_required(login_url='/login')
def declinereq(request,senderid):
    receiveruser=user_profile.getUserProfileByUserId(request.user)
    senderuser=user_profile.getUserProfileById(senderid)
    friendreq=Friend_request.getReceiverFriendRequest(receiveruser)
    for friend in friendreq:
        if friend.sender_user == senderuser:
            # print(friend.sender_user)
            print(friend.sender_user)
            friend.delete()
    print(friend)
    return redirect('/editprofile')

@login_required(login_url='/login')
def edit_req(request,senderid):
    if request.method=='POST':
        user1=user_profile.getUserProfileByUserId(request.user)
        user=User.objects.get(username=request.user)
        print("user is :" ,user)
        username=request.POST.get('username')
        # password=request.POST.get('password') frnz_username
        gender=request.POST.get('gender')
        frnz_username=request.POST.get('frnz_username')
        email=request.POST.get('email')
        collage=request.POST.get('collage')
        branch=request.POST.get('branch')
        # print(email,collage,branch)
        user1.user.email=email
        user1.branch=branch
        user1.collage=collage
        user1.user.username=frnz_username
        user.username=frnz_username
        print(user1.user.username)
        user1.gender=gender
        user1.save()
        user.save()
        return redirect("editprofile")
    else:
        print("nope")

@login_required(login_url='/login')
def change_about(request):
    if request.method=='POST':    
        user1=user_profile.getUserProfileByUserId(request.user)
        about=request.POST['about']
        user1.about=about
        user1.save()
        # print(about)
        return redirect("editprofile")
