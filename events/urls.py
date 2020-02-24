from django.urls import path

from . import views

app_name = "talks"

urlpatterns = [
    path("<int:id>/", views.TalkDetail.as_view(), name="talk-detail"),
    path("<int:id>/pdf", views.TalkPdfDetail.as_view(), name="talk-pdf"),
    path("<int:id>/edit", views.TalkEdit.as_view(), name="talk-edit"),
    path("add/", views.TalkAdd.as_view(), name="add"),
    path("", views.TalkList.as_view(), name="list"),
]
