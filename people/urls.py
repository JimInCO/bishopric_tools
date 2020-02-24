from django.urls import path

from . import views

app_name = "members"
urlpatterns = [
    path("", views.MemberList.as_view(), name="list"),
    path("add", views.MemberAddView.as_view(), name="add"),
    path("<int:pk>/", views.MemberDetail.as_view(), name="detail"),
]
