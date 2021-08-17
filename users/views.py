from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from django.utils.translation import gettext as _
from .models import User, Friend_Request
from .forms import UserCreateForm

def signup(request):
    """Sign up view"""
    print(request.method)
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            print('Valid')
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('user_home')
        else:
            print('not valid')
            print(request.POST, form.errors)
            return render(request, 'users/signup.html', {'form': form, 'error': form.errors})
    else:
        form = UserCreateForm()
        return render(request, 'users/signup.html', {'form': form})
        

def login_view(request):
    """Login view"""
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user is not None:
            login(request, user)
            #return HttpResponse('Logged in')
            return redirect('user_home')
        else:
            return HttpResponse('Login Unsuccessfull')
    else: 
        # return render(request, 'users/login.html')
        template = loader.get_template('users/login.html')
        return HttpResponse(template.render({}, request))

@login_required
def logout_view(request):
    """Logout veiw"""
    logout(request)
    return redirect('user_home')


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

def user_home(request):
    context = {
        'title': _('UserHome'),
        'user': request.user
    }
    template = loader.get_template('users/homepage.html')
    return HttpResponse(template.render(context, request))

