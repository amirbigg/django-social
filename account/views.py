from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm, PhoneLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from posts.models import Post
from django.contrib.auth.decorators import login_required
from random import randint
from kavenegar import *


def user_login(request):
	next = request.GET.get('next')
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'success')
				if next:
					return redirect(next)
				return redirect('posts:all_posts')
			else:
				messages.error(request, 'wrong username or password', 'warning')
	else:
		form = UserLoginForm()
	return render(request, 'account/login.html', {'form':form})


def user_register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
			login(request, user)
			messages.success(request, 'you registered successfully', 'success')
			return redirect('posts:all_posts')
	else:
		form = UserRegistrationForm()
	return render(request, 'account/register.html', {'form':form})

@login_required
def user_logout(request):
	logout(request)
	messages.success(request, 'you logged out successfully', 'success')
	return redirect('posts:all_posts')

@login_required
def user_dashboard(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	posts = Post.objects.filter(user=user)
	self_dash = False
	if request.user.id == user_id:
		self_dash = True
	return render(request, 'account/dashboard.html', {'user':user, 'posts':posts, 'self_dash':self_dash})



@login_required
def edit_profile(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=user.profile)
		if form.is_valid():
			form.save()
			user.email = form.cleaned_data['email']
			user.save()
			messages.success(request, 'your profile edited successfully', 'success')
			return redirect('account:dashboard', user_id)
	else:
		form = EditProfileForm(instance=user.profile, initial={'email':request.user.email})
	return render(request, 'account/edit_profile.html', {'form':form})


def phone_login(request):
	if request.method == 'POST':
		form = PhoneLoginForm(request.POST)
		if form.is_valid():
			phone = f"0{form.cleaned_data['phone']}"
			rand_num = randint(1000, 9999)
			api = KavenegarAPI('54624B564154623558564355506C59417230747550612F7456524A544F4B733535374A624830485856456B3D')
			params = {'sender':'', 'receptor':phone, 'message':rand_num}
			api.sms_send(params)
			# return redirect('account:verify', phone, rand_num)
	else:
		form = PhoneLoginForm()
	return render(request, 'account/phone_login.html', {'form':form})












