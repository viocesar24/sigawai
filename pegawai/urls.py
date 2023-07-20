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
    path(
        "download_ijazah/<int:id_pendidikan>/",
        login_required(views.download_ijazah),
        name="download_ijazah",
    ),
    path("add_jabatan/", login_required(views.add_jabatan), name="add_jabatan"),
    path(
        "edit_jabatan/<int:id_jabatan>/",
        login_required(views.edit_jabatan),
        name="edit_jabatan",
    ),
    path(
        "delete_jabatan/<int:id_jabatan>/",
        login_required(views.delete_jabatan),
        name="delete_jabatan",
    ),
    path(
        "download_sk_jabatan/<int:id_jabatan>/",
        login_required(views.download_sk_jabatan),
        name="download_sk_jabatan",
    ),
]
