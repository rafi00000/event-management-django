from django.urls import path, include
from users.views import sign_in, sign_out, sign_up, activate_account

urlpatterns = [
    path("sign-up/", sign_up, name="sign-up"),
    path("sign-in/", sign_in, name="sign-in"),
    path("sign-out/", sign_out, name="sign-out"),
    path("activate/<int:user_id>/<str:token>/", activate_account, name="activate-account")
]