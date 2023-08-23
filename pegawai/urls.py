from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("beranda/", views.index, name="index"),
    path("signout/", views.signout, name="signout"),
    path("profil/", views.profile, name="profile"),
    ##### PEGAWAI #####
    path("add_pegawai/", login_required(views.add_pegawai), name="add_pegawai"),
    path(
        "add_data_pegawai/",
        login_required(views.add_data_pegawai),
        name="add_data_pegawai",
    ),
    path(
        "edit_pegawai/<int:id_pegawai>/",
        login_required(views.edit_pegawai),
        name="edit_pegawai",
    ),
    path(
        "delete_pegawai/<int:id_pegawai>/",
        login_required(views.delete_pegawai),
        name="delete_pegawai",
    ),
    ##### PENDIDIKAN #####
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
    ##### JABATAN #####
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
    ##### PANGKAT & GOLONGAN #####
    path("add_pangkat/", login_required(views.add_pangkat), name="add_pangkat"),
    path(
        "edit_pangkat/<int:id_pangkat>/",
        login_required(views.edit_pangkat),
        name="edit_pangkat",
    ),
    path(
        "delete_pangkat/<int:id_pangkat>/",
        login_required(views.delete_pangkat),
        name="delete_pangkat",
    ),
    path(
        "download_sk_pangkat/<int:id_pangkat>/",
        login_required(views.download_sk_pangkat),
        name="download_sk_pangkat",
    ),
    ##### PENILAIAN ANGKA KREDIT #####
    path("add_pak/", login_required(views.add_pak), name="add_pak"),
    path(
        "edit_pak/<int:id_pak>/",
        login_required(views.edit_pak),
        name="edit_pak",
    ),
    path(
        "delete_pak/<int:id_pak>/",
        login_required(views.delete_pak),
        name="delete_pak",
    ),
    path(
        "download_file_pak/<int:id_pak>/",
        login_required(views.download_file_pak),
        name="download_file_pak",
    ),
    ##### DIKLAT #####
    path("add_diklat/", login_required(views.add_diklat), name="add_diklat"),
    path(
        "edit_diklat/<int:id_diklat>/",
        login_required(views.edit_diklat),
        name="edit_diklat",
    ),
    path(
        "delete_diklat/<int:id_diklat>/",
        login_required(views.delete_diklat),
        name="delete_diklat",
    ),
    path(
        "download_file_diklat/<int:id_diklat>/",
        login_required(views.download_file_diklat),
        name="download_file_diklat",
    ),
    ##### EKSPOR IMPOR EXCEL #####
    path(
        "export_to_excel/",
        login_required(views.export_to_excel),
        name="export_to_excel",
    ),
    path(
        "import_from_excel/",
        login_required(views.import_from_excel),
        name="import_from_excel",
    ),
    ##### HALAMAN ADMIN #####
    path(
        "administrasi/",
        login_required(views.administrasi),
        name="administrasi",
    ),
    ##### USER #####
    path("add_user/", login_required(views.add_user), name="add_user"),
    path(
        "edit_user/<int:user_id>/",
        login_required(views.edit_user),
        name="edit_user",
    ),
    path(
        "delete_user/<int:user_id>/",
        login_required(views.delete_user),
        name="delete_user",
    ),
]
