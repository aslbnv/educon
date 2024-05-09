from authy.models import Profile
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.db.models import Sum
from django.db import transaction

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from django.core.paginator import Paginator


def SideNavInfo(request):
	user = request.user
	nav_profile = None

	if user.is_authenticated:
		nav_profile = Profile.objects.get(user=user)
	
	return {'nav_profile': nav_profile}


def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)

	template = loader.get_template('registration/user_details.html')

	context = {
		'profile': profile,
	}

	return HttpResponse(template.render(context, request))


def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			User.objects.create_user(username=username, email=email, password=password,
			first_name=first_name, last_name=last_name)
			return redirect('edit-profile')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'registration/signup.html', context)


@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'registration/change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
	user = request.user
	user_id = request.user.id
	profile = Profile.objects.get(user__id=user_id)
	user_info = User.objects.get(id=user_id)
	initial_data = {'first_name': user.first_name, 'last_name': user.last_name}

	if request.method == 'POST':
		form = EditProfileForm(request.POST, initial=initial_data)
		if form.is_valid():
			user_info.first_name = form.cleaned_data.get('first_name')
			user_info.last_name = form.cleaned_data.get('last_name')
			profile.save()
			user_info.save()
			return redirect('index')
	else:
		init_data = {'first_name': user.first_name, 'last_name': user.last_name}
		form = EditProfileForm(initial=init_data)

	context = {
		'form': form,
		'profile': profile,
		'user': user,
	}

	return render(request, 'registration/user_details.html', context)