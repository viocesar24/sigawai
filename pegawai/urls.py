from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("beranda/", views.index, name="index"),
    path("signout/", views.signout, name="signout"),
    path("profil/", views.profile, name="profile"),
    path("add_pegawai/", login_required(views.add_pegawai), name="add_pegawai"),
    path(
        "add_pendidikan/", login_required(views.add_pendidikan), name="add_pendidikan"
    ),
    path(
        "edit_pendidikan/<int:id_pendidikan>/",
        login_required(views.edit_pendidikan),
        name="edit_pendidikan",
    ),
    path(
        "delete_pendidikan/<int:id_pendidikan>/",
        login_required(views.delete_pendidikan),
        name="delete_pendidikan",
    ),
]
