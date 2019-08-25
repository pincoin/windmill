from importlib import import_module

from allauth.socialaccount import providers
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

    # Social Providers
    path('social/login/cancelled/',
         views.MemberSocialLoginCancelledView.as_view(), name='socialaccount_login_cancelled'),
    path('social/login/error/',
         views.MemberSocialLoginErrorView.as_view(), name='socialaccount_login_error'),
    path('social/signup/',
         views.MemberSocialSignupView.as_view(), name='socialaccount_signup'),
    path('social/connections/',
         views.MemberSocialConnectionsView.as_view(), name='socialaccount_connections'),

    # Profile
    path('profile/',
         views.MemberProfileView.as_view(), name="account_profile"),
    path('profile/logs/',
         views.MemberLoginLogView.as_view(), name="account_login_log"),
    path('profile/organization/',
         views.MemberOrganizationCreateView.as_view(), name="account_organization"),

]

# URL patterns for social providers
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        urlpatterns += prov_urlpatterns
