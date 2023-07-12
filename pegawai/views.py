from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Selamat datang di Halaman Pegawai aplikasi SiGawai.")
