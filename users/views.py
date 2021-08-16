from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Friend_Request
from django.contrib.auth.decorators import login_required
from .forms import UserCreateForm

def signup(request):
    """Sign up view"""
    if request.method == "POST":
        form = UserCreateForm(request.Post)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            login(request, new_user)
        else:
            pritn(request.POST, form.errors)
            return render(request, 'signup.html', {'form': form, 'error': form.errors})
    else:
        form = UserCreateForm()
        return render(request, 'users/signup.html', {'form': form})

def login(request):
    """Login view"""
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user is not None:
            login(request, user)
            return HttpResponse('Logged in')
        else:
            return HttpResponse('Login Unsuccessfull')
    else: 
        return render(request, 'users/login.html')

@login_required
def send_friend_request(request, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('Friend request sent')
    else:
        return HttpResponse('Friend request was already sent')

@login_required
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('Friend request accepted')
    else:
        return HttpResponse('Friend request not accepted')

