from django.urls import (
    path, re_path
)

from . import views

urlpatterns = [
    # Account
    path('login/',
         views.MemberLoginView.as_view(), name="account_login"),
    path('logout/',
         views.MemberLogoutView.as_view(), name="account_logout"),
    path('signup/',
         views.MemberSignupView.as_view(), name="account_signup"),

    # Password Change
    path('password/change/',
         views.MemberLoginView.as_view(), name="account_change_password"),

    # Password Reset
    path('password/reset/',
         views.MemberLoginView.as_view(), name="account_reset_password"),

    # Email Confirmation
    path('confirm-email/',
         views.MemberLoginView.as_view(), name="account_email_verification_sent"),
    re_path(r'^confirm-email/(?P<key>[-:\w]+)/$',
            views.MemberLoginView.as_view(), name="account_confirm_email"),
    path('email/',
         views.MemberLoginView.as_view(), name="account_email"),

    # Profile
]

'''
# Account

path('signup/',
     views.MemberSignupView.as_view(), name="account_signup"),
path('inactive/',
     views.MemberAccountInactiveView.as_view(), name="account_inactive"),
path('unregister/',
     views.MemberUnregisterView.as_view(), name="account_unregister"),

# Password Change
path('password/change/',
     views.MemberPasswordChangeView.as_view(), name="account_change_password"),
path('password/set/',
     views.MemberPasswordSetView.as_view(), name="account_set_password"),

# Password Reset
path('password/reset/',
     views.MemberPasswordReset.as_view(), name="account_reset_password"),
path('password/reset/done/',
     views.MemberPasswordResetDoneView.as_view(), name="account_reset_password_done"),
re_path(r'^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
        views.MemberPasswordResetFromKeyView.as_view(), name="account_reset_password_from_key"),
path('password/reset/key/done/',
     views.MemberPasswordResetFromKeyDoneView.as_view(), name="account_reset_password_from_key_done"),

# Email Confirmation
path('confirm-email/',
     views.MemberEmailVerificationSentView.as_view(), name="account_email_verification_sent"),
re_path(r'^confirm-email/(?P<key>[-:\w]+)/$',
        views.MemberConfirmEmailView.as_view(), name="account_confirm_email"),
path('email/',
     views.MemberEmailView.as_view(), name="account_email"),

# Profile
path('profile/',
     views.MemberProfileView.as_view(), name="account_profile"),
path('change-name/',
     views.MemberLoginView.as_view(), name="account_change_name"),
     '''
