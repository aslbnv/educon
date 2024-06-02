from authy.models import Profile
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def sign_up(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            return redirect("profile")
    else:
        form = SignupForm()

    context = {
        "form": form,
    }

    return render(request, "registration/signup.html", context)


@login_required
def change_password(request):
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect("password-change-done")
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        "form": form,
    }

    return render(request, "registration/change_password.html", context)


@login_required
def password_change_done(request):
    return render(request, "change_password_done.html")


@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get(user__id=user.id)
    init_data = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "patronymic": profile.patronymic,
        "email": user.email,
    }

    if request.method == "POST":
        form = EditProfileForm(request.POST, initial=init_data)
        if form.is_valid():
            user.username = form.cleaned_data.get("username")
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.email = form.cleaned_data.get("email")
            profile.patronymic = form.cleaned_data.get("patronymic")

            user.save()
            profile.save()
            return redirect("index")
    else:
        form = EditProfileForm(initial=init_data)

    context = {
        "form": form,
        "profile": profile,
        "user": user,
    }

    return render(request, "registration/user_data.html", context)
