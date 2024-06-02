from django.urls import path
from django.contrib.auth import views as authViews 

from authy.views import (
    UserProfile,
    sign_up,
    change_password,
    password_change_done,
    profile,
)

urlpatterns = [
    path('profile', profile, name='profile'),
   	path('auth/signup', sign_up, name='sign-up'),
   	path('auth/login', authViews.LoginView.as_view(template_name='registration/login.html'), name='login'),
   	path('auth/logout', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
   	path('password/change', change_password, name='change-password'),
   	path('password/change/done', password_change_done, name='password-change-done'),
   	path('password/reset', authViews.PasswordResetView.as_view(), name='password-reset'),
   	path('password/reset/done', authViews.PasswordResetDoneView.as_view(), name='password-reset-done'),
   	path('password/reset/<uidb64>/<token>', authViews.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
   	path('password/reset/complete', authViews.PasswordResetCompleteView.as_view(), name='password-reset-complete'),
]
