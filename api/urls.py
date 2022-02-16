from django.urls import path
from .views import Action, SignUpView, LogInView, Dashboard
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LogInView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path("verify/", TokenVerifyView.as_view()),
    path('dashboard/', Dashboard.as_view()),
    path('action/<int:id>/', Action.as_view()),
]
