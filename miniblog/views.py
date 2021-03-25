from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import post
from django.contrib.auth.models import Group

#home method.
def home(request):
    posts = post.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})

#About method
def about(request):
    return render(request, 'blog/about.html')

#Contact method
def contact(request):
    return render(request, 'blog/contact.html')

#Dashboard method
def dashboard(request):
    if request.user.is_authenticated:
        posts = post.objects.all()
        return render(request, 'blog/dashboard.html',{'posts':posts})
    else:
        return HttpResponseRedirect('/login/')

#Logout method

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

#Contact method
def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'congrats! now you have been an author. feel free to do good posts.')
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)


    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form':form})

#Contact method
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in successfully!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')



#Add Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=PostForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst=post(title=title,desc=desc)
                pst.save()
                form=PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/add.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


#Update post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method =='POST':
            pi = post.objects.get(pk=id)
            form=PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = post.objects.get(pk=id)
            form=PostForm(instance=pi)
        return render(request, 'blog/update.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

#delete post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

  
