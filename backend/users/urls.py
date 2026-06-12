from django.urls import path
from .views import UserListView, UserDetailView, ChangePasswordView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/password/', ChangePasswordView.as_view(), name='change-password'),
]
