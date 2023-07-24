from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import HttpResponse, Http404
from .models import Pegawai, Pendidikan, Jabatan, Pangkat, AngkaKredit, Diklat
import os
import json


def index(request):
    # Mendapatkan username user yang sedang login
    username = request.user.username

    ##### PEGAWAI #####
    # Mendapatkan data pegawai dari user yang sedang login
    try:
        # Mengambil data tabel pegawai
        pegawai = Pegawai.objects.get(user=request.user)
        # Ubah format tanggal lahir menjadi "YYYY/MM/DD"
        tanggal_lahir_pegawai = pegawai.tanggal_lahir_pegawai.strftime("%Y-%m-%d")
    except Pegawai.DoesNotExist:
        # Jika data tabel pegawai tidak ada maka return Null/None
        pegawai = None
        tanggal_lahir_pegawai = None

    ##### PENDIDIKAN #####
    # Mendapatkan data pendidikan dari user yang sedang login
    try:
        # Mengambil data tabel pendidikan
        pendidikan = Pendidikan.objects.filter(user=request.user).order_by(
            "-tanggal_terbit_ijazah_pendidikan"
        )
        if pendidikan.exists():
            pendidikan_terakhir = pendidikan[0]
        else:
            pendidikan_terakhir = None
    except Pendidikan.DoesNotExist:
        # Jika data tabel pendidikan tidak ada maka return Null/None
        pendidikan = None
        pendidikan_terakhir = None

    # Inisialisasi file_exists_pendidikan sebagai False
    file_exists_pendidikan = False

    if pendidikan.exists():
        # Ubah format tanggal terbit ijazah pendidikan menjadi "YYYY/MM/DD"
        for pend in pendidikan:
            pend.tanggal_terbit_ijazah_pendidikan = (
                pend.tanggal_terbit_ijazah_pendidikan.strftime("%Y-%m-%d")
            )
            if pend and pend.file_ijazah_pendidikan:
                file_exists_pendidikan = default_storage.exists(
                    pend.file_ijazah_pendidikan.name
                )
            else:
                # Keluar dari loop jika file_exists_pendidikan telah ditemukan
                break

    # Mengambil data pilihan tingkat pendidikan
    pilihan_tingkat_pendidikan = Pendidikan.TingkatPendidikan.choices

    ##### JABATAN #####
    # Mendapatkan data jabatan dari user yang sedang login
    try:
        # Mengambil data tabel jabatan
        jabatan = Jabatan.objects.filter(user=request.user).order_by(
            "-tanggal_sk_jabatan"
        )
        if jabatan.exists():
            jabatan_terakhir = jabatan[0]
        else:
            jabatan_terakhir = None
    except Jabatan.DoesNotExist:
        # Jika data tabel jabatan tidak ada maka return Null/None
        jabatan = None
        jabatan_terakhir = None

    # Inisialisasi file_exists_jabatan sebagai False
    file_exists_jabatan = False

    if jabatan.exists():
        # Ubah format tanggal sk jabatan menjadi "YYYY/MM/DD"
        for jab in jabatan:
            jab.tanggal_sk_jabatan = jab.tanggal_sk_jabatan.strftime("%Y-%m-%d")
            jab.tmt_jabatan = jab.tmt_jabatan.strftime("%Y-%m-%d")
            if jab and jab.file_sk_jabatan:
                file_exists_jabatan = default_storage.exists(jab.file_sk_jabatan.name)
            else:
                # Keluar dari loop jika file_exists_jabatan telah ditemukan
                break

    # Mengambil data pilihan jabatan
    pilihan_jabatan = Jabatan.NamaJabatan.choices

    ##### PANGKAT #####
    # Mendapatkan data pangkat dari user yang sedang login
    try:
        # Mengambil data tabel pangkat
        pangkat = Pangkat.objects.filter(user=request.user).order_by(
            "-tanggal_sk_pangkat"
        )
        if pangkat.exists():
            pangkat_terakhir = pangkat[0]
        else:
            pangkat_terakhir = None
    except Pangkat.DoesNotExist:
        # Jika data tabel pangkat tidak ada maka return Null/None
        pangkat = None
        pangkat_terakhir = None

    # Inisialisasi file_exists_pangkat sebagai False
    file_exists_pangkat = False

    if pangkat.exists():
        # Ubah format tanggal sk pangkat menjadi "YYYY/MM/DD"
        for pang in pangkat:
            pang.tanggal_sk_pangkat = pang.tanggal_sk_pangkat.strftime("%Y-%m-%d")
            pang.tmt_pangkat = pang.tmt_pangkat.strftime("%Y-%m-%d")
            if pang and pang.tanggal_sk_pangkat:
                file_exists_pangkat = default_storage.exists(pang.file_sk_pangkat.name)
            else:
                # Keluar dari loop jika file_exists_pangkat telah ditemukan
                break

    # Mengambil data pilihan pangkat
    pilihan_pangkat = Pangkat.KodePangkat.choices

    ##### PENILAIAN ANGKA KREDIT (PAK) #####
    # Mendapatkan data PAK dari user yang sedang login
    try:
        # Mengambil data tabel PAK
        pak = AngkaKredit.objects.filter(user=request.user).order_by("-tanggal_pak")
        if pak.exists():
            pak_terakhir = pak[0]
        else:
            pak_terakhir = None
    except AngkaKredit.DoesNotExist:
        # Jika data tabel PAK tidak ada maka return Null/None
        pak = None
        pak_terakhir = None

    # Inisialisasi file_exists_pak sebagai False
    file_exists_pak = False

    # Mengambil data PAK untuk dimasukkan ke dalam chart
    pak_data = []

    if pak.exists():
        # Ubah format tanggal PAK menjadi "YYYY/MM/DD"
        for ak in pak:
            ak.tanggal_pak = ak.tanggal_pak.strftime("%Y-%m-%d")
            pak_data.append(
                {
                    "tanggal_pak": ak.tanggal_pak,
                    "nilai_pak": ak.nilai_pak,
                }
            )
            if ak and ak.tanggal_pak:
                file_exists_pak = default_storage.exists(ak.file_pak.name)
            else:
                # Keluar dari loop jika file_exists_pak telah ditemukan
                break

    # Mengubah data menjadi JSON
    pak_data_json = json.dumps(pak_data)

    # Mengambil data pilihan PAK
    pilihan_pak = AngkaKredit.MasaPenilaian.choices

    ##### DIKLAT #####
    # Mendapatkan data DIKLAT dari user yang sedang login
    try:
        # Mengambil data tabel DIKLAT
        diklat = Diklat.objects.filter(user=request.user).order_by(
            "-tanggal_sertifikat_diklat"
        )
        if diklat.exists():
            diklat_terakhir = diklat[0]
        else:
            diklat_terakhir = None
    except Diklat.DoesNotExist:
        # Jika data tabel DIKLAT tidak ada maka return Null/None
        diklat = None
        diklat_terakhir = None

    # Inisialisasi file_exists_dik sebagai False
    file_exists_diklat = False

    if diklat.exists():
        # Ubah format tanggal sertifikat DIKLAT, tanggal mulai dan selesai DIKLAT menjadi "YYYY/MM/DD"
        for dik in diklat:
            dik.tanggal_mulai_diklat = dik.tanggal_mulai_diklat.strftime("%Y-%m-%d")
            dik.tanggal_selesai_diklat = dik.tanggal_selesai_diklat.strftime("%Y-%m-%d")
            dik.tanggal_sertifikat_diklat = dik.tanggal_sertifikat_diklat.strftime(
                "%Y-%m-%d"
            )
            if dik and dik.tanggal_sertifikat_diklat:
                file_exists_diklat = default_storage.exists(
                    dik.file_sertifikat_diklat.name
                )
            else:
                # Keluar dari loop jika file_exists_diklat telah ditemukan
                break

    context = {
        "username": username,
        "pegawai": pegawai,
        "tanggal_lahir_pegawai": tanggal_lahir_pegawai,
        "pendidikan": pendidikan,
        "pendidikan_terakhir": pendidikan_terakhir,
        "pilihan_tingkat_pendidikan": pilihan_tingkat_pendidikan,
        "file_exists_pendidikan": file_exists_pendidikan,
        "jabatan": jabatan,
        "jabatan_terakhir": jabatan_terakhir,
        "pilihan_jabatan": pilihan_jabatan,
        "file_exists_jabatan": file_exists_jabatan,
        "pangkat": pangkat,
        "pangkat_terakhir": pangkat_terakhir,
        "pilihan_pangkat": pilihan_pangkat,
        "file_exists_pangkat": file_exists_pangkat,
        "pak": pak,
        "pak_terakhir": pak_terakhir,
        "pilihan_pak": pilihan_pak,
        "file_exists_pak": file_exists_pak,
        "pak_data_json": pak_data_json,  # Menambahkan data JSON ke konteks
        "diklat": diklat,
        "diklat_terakhir": diklat_terakhir,
        "file_exists_diklat": file_exists_diklat,
    }
    return render(request, "pegawai/index.html", context)


@login_required
def profile(request):
    # Mendapatkan username user yang sedang login
    username = request.user.username

    ##### PEGAWAI #####
    # Mendapatkan data pegawai dari user yang sedang login
    try:
        # Mengambil data tabel pegawai
        pegawai = Pegawai.objects.get(user=request.user)
        # Ubah format tanggal lahir menjadi "YYYY/MM/DD"
        tanggal_lahir_pegawai = pegawai.tanggal_lahir_pegawai.strftime("%Y-%m-%d")
    except Pegawai.DoesNotExist:
        # Jika data tabel pegawai tidak ada maka return Null/None
        pegawai = None
        tanggal_lahir_pegawai = None

    ##### PENDIDIKAN #####
    # Mendapatkan data pendidikan dari user yang sedang login
    try:
        # Mengambil data tabel pendidikan
        pendidikan = Pendidikan.objects.filter(user=request.user).order_by(
            "-tanggal_terbit_ijazah_pendidikan"
        )
        if pendidikan.exists():
            pendidikan_terakhir = pendidikan[0]
        else:
            pendidikan_terakhir = None
    except Pendidikan.DoesNotExist:
        # Jika data tabel pendidikan tidak ada maka return Null/None
        pendidikan = None
        pendidikan_terakhir = None

    # Inisialisasi file_exists_pendidikan sebagai False
    file_exists_pendidikan = False

    if pendidikan.exists():
        # Ubah format tanggal terbit ijazah pendidikan menjadi "YYYY/MM/DD"
        for pend in pendidikan:
            pend.tanggal_terbit_ijazah_pendidikan = (
                pend.tanggal_terbit_ijazah_pendidikan.strftime("%Y-%m-%d")
            )
            if pend and pend.file_ijazah_pendidikan:
                file_exists_pendidikan = default_storage.exists(
                    pend.file_ijazah_pendidikan.name
                )
            else:
                # Keluar dari loop jika file_exists_pendidikan telah ditemukan
                break

    # Mengambil data pilihan tingkat pendidikan
    pilihan_tingkat_pendidikan = Pendidikan.TingkatPendidikan.choices

    ##### JABATAN #####
    # Mendapatkan data jabatan dari user yang sedang login
    try:
        # Mengambil data tabel jabatan
        jabatan = Jabatan.objects.filter(user=request.user).order_by(
            "-tanggal_sk_jabatan"
        )
        if jabatan.exists():
            jabatan_terakhir = jabatan[0]
        else:
            jabatan_terakhir = None
    except Jabatan.DoesNotExist:
        # Jika data tabel jabatan tidak ada maka return Null/None
        jabatan = None
        jabatan_terakhir = None

    # Inisialisasi file_exists_jabatan sebagai False
    file_exists_jabatan = False

    if jabatan.exists():
        # Ubah format tanggal sk jabatan menjadi "YYYY/MM/DD"
        for jab in jabatan:
            jab.tanggal_sk_jabatan = jab.tanggal_sk_jabatan.strftime("%Y-%m-%d")
            jab.tmt_jabatan = jab.tmt_jabatan.strftime("%Y-%m-%d")
            if jab and jab.file_sk_jabatan:
                file_exists_jabatan = default_storage.exists(jab.file_sk_jabatan.name)
            else:
                # Keluar dari loop jika file_exists_jabatan telah ditemukan
                break

    # Mengambil data pilihan jabatan
    pilihan_jabatan = Jabatan.NamaJabatan.choices

    ##### PANGKAT #####
    # Mendapatkan data pangkat dari user yang sedang login
    try:
        # Mengambil data tabel pangkat
        pangkat = Pangkat.objects.filter(user=request.user).order_by(
            "-tanggal_sk_pangkat"
        )
        if pangkat.exists():
            pangkat_terakhir = pangkat[0]
        else:
            pangkat_terakhir = None
    except Pangkat.DoesNotExist:
        # Jika data tabel pangkat tidak ada maka return Null/None
        pangkat = None
        pangkat_terakhir = None

    # Inisialisasi file_exists_pangkat sebagai False
    file_exists_pangkat = False

    if pangkat.exists():
        # Ubah format tanggal sk pangkat menjadi "YYYY/MM/DD"
        for pang in pangkat:
            pang.tanggal_sk_pangkat = pang.tanggal_sk_pangkat.strftime("%Y-%m-%d")
            pang.tmt_pangkat = pang.tmt_pangkat.strftime("%Y-%m-%d")
            if pang and pang.tanggal_sk_pangkat:
                file_exists_pangkat = default_storage.exists(pang.file_sk_pangkat.name)
            else:
                # Keluar dari loop jika file_exists_pangkat telah ditemukan
                break

    # Mengambil data pilihan pangkat
    pilihan_pangkat = Pangkat.KodePangkat.choices

    ##### PENILAIAN ANGKA KREDIT (PAK) #####
    # Mendapatkan data PAK dari user yang sedang login
    try:
        # Mengambil data tabel PAK
        pak = AngkaKredit.objects.filter(user=request.user).order_by("-tanggal_pak")
        if pak.exists():
            pak_terakhir = pak[0]
        else:
            pak_terakhir = None
    except AngkaKredit.DoesNotExist:
        # Jika data tabel PAK tidak ada maka return Null/None
        pak = None
        pak_terakhir = None

    # Inisialisasi file_exists_pak sebagai False
    file_exists_pak = False

    # Mengambil data PAK untuk dimasukkan ke dalam chart
    pak_data = []

    if pak.exists():
        # Ubah format tanggal PAK menjadi "YYYY/MM/DD"
        for ak in pak:
            ak.tanggal_pak = ak.tanggal_pak.strftime("%Y-%m-%d")
            pak_data.append(
                {
                    "tanggal_pak": ak.tanggal_pak,
                    "nilai_pak": ak.nilai_pak,
                }
            )
            if ak and ak.tanggal_pak:
                file_exists_pak = default_storage.exists(ak.file_pak.name)
            else:
                # Keluar dari loop jika file_exists_pak telah ditemukan
                break

    # Mengubah data menjadi JSON
    pak_data_json = json.dumps(pak_data)

    # Mengambil data pilihan PAK
    pilihan_pak = AngkaKredit.MasaPenilaian.choices

    ##### DIKLAT #####
    # Mendapatkan data DIKLAT dari user yang sedang login
    try:
        # Mengambil data tabel DIKLAT
        diklat = Diklat.objects.filter(user=request.user).order_by(
            "-tanggal_sertifikat_diklat"
        )
        if diklat.exists():
            diklat_terakhir = diklat[0]
        else:
            diklat_terakhir = None
    except Diklat.DoesNotExist:
        # Jika data tabel DIKLAT tidak ada maka return Null/None
        diklat = None
        diklat_terakhir = None

    # Inisialisasi file_exists_dik sebagai False
    file_exists_diklat = False

    if diklat.exists():
        # Ubah format tanggal sertifikat DIKLAT, tanggal mulai dan selesai DIKLAT menjadi "YYYY/MM/DD"
        for dik in diklat:
            dik.tanggal_mulai_diklat = dik.tanggal_mulai_diklat.strftime("%Y-%m-%d")
            dik.tanggal_selesai_diklat = dik.tanggal_selesai_diklat.strftime("%Y-%m-%d")
            dik.tanggal_sertifikat_diklat = dik.tanggal_sertifikat_diklat.strftime(
                "%Y-%m-%d"
            )
            if dik and dik.tanggal_sertifikat_diklat:
                file_exists_diklat = default_storage.exists(
                    dik.file_sertifikat_diklat.name
                )
            else:
                # Keluar dari loop jika file_exists_diklat telah ditemukan
                break

    context = {
        "username": username,
        "pegawai": pegawai,
        "tanggal_lahir_pegawai": tanggal_lahir_pegawai,
        "pendidikan": pendidikan,
        "pendidikan_terakhir": pendidikan_terakhir,
        "pilihan_tingkat_pendidikan": pilihan_tingkat_pendidikan,
        "file_exists_pendidikan": file_exists_pendidikan,
        "jabatan": jabatan,
        "jabatan_terakhir": jabatan_terakhir,
        "pilihan_jabatan": pilihan_jabatan,
        "file_exists_jabatan": file_exists_jabatan,
        "pangkat": pangkat,
        "pangkat_terakhir": pangkat_terakhir,
        "pilihan_pangkat": pilihan_pangkat,
        "file_exists_pangkat": file_exists_pangkat,
        "pak": pak,
        "pak_terakhir": pak_terakhir,
        "pilihan_pak": pilihan_pak,
        "file_exists_pak": file_exists_pak,
        "pak_data_json": pak_data_json,  # Menambahkan data JSON ke konteks
        "diklat": diklat,
        "diklat_terakhir": diklat_terakhir,
        "file_exists_diklat": file_exists_diklat,
    }
    return render(request, "pegawai/profile.html", context)


def signin(request):
    if request.user.is_authenticated:
        return redirect("index")  # User sudah signin, arahkan ke index

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Username atau password salah.")

    return render(request, "pegawai/signin.html")


@login_required
def signout(request):
    logout(request)
    return redirect("signin")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(
                    request, "Username sudah terdaftar. Silakan gunakan username lain."
                )
            else:
                # Buat user baru
                User.objects.create_user(username=username, password=password)
                messages.success(request, "Anda berhasil mendaftar, silahkan login.")
                return redirect("signin")
            # Ganti 'home' dengan URL halaman setelah sign up
        else:
            messages.error(request, "Password tidak sesuai.")

    return render(request, "pegawai/signup.html")


##### PEGAWAI #####
@login_required
def add_pegawai(request):
    user_id = request.user.id

    if request.method == "POST":
        aktif_pegawai = request.POST["aktif_pegawai"]
        nip_pegawai = request.POST["nip_pegawai"]
        nama_pegawai = request.POST["nama_pegawai"]
        tempat_lahir_pegawai = request.POST["tempat_lahir_pegawai"]
        tanggal_lahir_pegawai = request.POST["tanggal_lahir_pegawai"]
        jenis_kelamin_pegawai = request.POST["jenis_kelamin_pegawai"]
        surel_pegawai = request.POST["surel_pegawai"]
        telepon_pegawai = request.POST["telepon_pegawai"]

        # Cek apakah sudah ada pegawai dengan user_id yang sama
        try:
            pegawai = Pegawai.objects.get(user_id=user_id)
            # Update data pegawai
            pegawai.aktif_pegawai = aktif_pegawai
            pegawai.nip_pegawai = nip_pegawai
            pegawai.nama_pegawai = nama_pegawai
            pegawai.tempat_lahir_pegawai = tempat_lahir_pegawai
            pegawai.tanggal_lahir_pegawai = tanggal_lahir_pegawai
            pegawai.jenis_kelamin_pegawai = jenis_kelamin_pegawai
            pegawai.surel_pegawai = surel_pegawai
            pegawai.telepon_pegawai = telepon_pegawai
            pegawai.save()
            messages.success(request, "Data pegawai berhasil diperbarui.")
        except Pegawai.DoesNotExist:
            # Buat pegawai baru
            Pegawai.objects.create(
                aktif_pegawai=aktif_pegawai,
                nip_pegawai=nip_pegawai,
                nama_pegawai=nama_pegawai,
                tempat_lahir_pegawai=tempat_lahir_pegawai,
                tanggal_lahir_pegawai=tanggal_lahir_pegawai,
                jenis_kelamin_pegawai=jenis_kelamin_pegawai,
                surel_pegawai=surel_pegawai,
                telepon_pegawai=telepon_pegawai,
                user_id=user_id,
            )
            messages.success(request, "Pegawai berhasil ditambahkan.")

        return redirect("profile")

    return render(request, "pegawai/profile.html")


##### PENDIDIKAN #####
@login_required
def add_pendidikan(request):
    user_id = request.user.id

    if request.method == "POST" and request.FILES["file_ijazah_pendidikan"]:
        tingkat_pendidikan = request.POST["tingkat_pendidikan"]
        lembaga_pendidikan = request.POST["lembaga_pendidikan"]
        fakultas_pendidikan = request.POST["fakultas_pendidikan"]
        jurusan_pendidikan = request.POST["jurusan_pendidikan"]
        gelar_depan_pendidikan = request.POST["gelar_depan_pendidikan"]
        gelar_belakang_pendidikan = request.POST["gelar_belakang_pendidikan"]
        nomor_seri_ijazah_pendidikan = request.POST["nomor_seri_ijazah_pendidikan"]
        tanggal_terbit_ijazah_pendidikan = request.POST[
            "tanggal_terbit_ijazah_pendidikan"
        ]
        file_ijazah_pendidikan = request.FILES["file_ijazah_pendidikan"]

        # Validasi tipe file
        if not file_ijazah_pendidikan.name.endswith(".pdf"):
            messages.error(request, "File harus berformat PDF.")
            return redirect("profile")

        # Validasi ukuran file
        max_size = 500 * 1024  # 500KB
        if file_ijazah_pendidikan.size > max_size:
            messages.error(request, "Ukuran file melebihi 500KB.")
            return redirect("profile")

        # Dapatkan username dari pengguna yang saat ini masuk
        username = request.user.username
        # Ubah nama file yang akan diunggah
        new_file_name = f"{username}_pendidikan_{tingkat_pendidikan}{file_ijazah_pendidikan.name[file_ijazah_pendidikan.name.rfind('.'):]}"
        fs = FileSystemStorage()

        try:
            Pendidikan.objects.get(
                tingkat_pendidikan=tingkat_pendidikan,
                nomor_seri_ijazah_pendidikan=nomor_seri_ijazah_pendidikan,
                user_id=user_id,
            )
            messages.warning(
                request,
                "Data Pendidikan sudah ada. Tolong gunakan fungsi edit.",
            )
            return redirect("profile")
        except Pendidikan.DoesNotExist:
            Pendidikan.objects.create(
                tingkat_pendidikan=tingkat_pendidikan,
                lembaga_pendidikan=lembaga_pendidikan,
                fakultas_pendidikan=fakultas_pendidikan,
                jurusan_pendidikan=jurusan_pendidikan,
                gelar_depan_pendidikan=gelar_depan_pendidikan,
                gelar_belakang_pendidikan=gelar_belakang_pendidikan,
                nomor_seri_ijazah_pendidikan=nomor_seri_ijazah_pendidikan,
                tanggal_terbit_ijazah_pendidikan=tanggal_terbit_ijazah_pendidikan,
                file_ijazah_pendidikan=fs.save(
                    f"media/pendidikan/{new_file_name}", file_ijazah_pendidikan
                ),
                user_id=user_id,
            )
            messages.success(request, "Data Pendidikan berhasil dibuat.")
            return redirect("profile")

    return render(request, "pegawai/profile.html")


@login_required
def edit_pendidikan(request, id_pendidikan):
    user_id = request.user.id

    if request.method == "POST" and request.FILES["file_ijazah_pendidikan"]:
        tingkat_pendidikan = request.POST["tingkat_pendidikan"]
        lembaga_pendidikan = request.POST["lembaga_pendidikan"]
        fakultas_pendidikan = request.POST["fakultas_pendidikan"]
        jurusan_pendidikan = request.POST["jurusan_pendidikan"]
        gelar_depan_pendidikan = request.POST["gelar_depan_pendidikan"]
        gelar_belakang_pendidikan = request.POST["gelar_belakang_pendidikan"]
        nomor_seri_ijazah_pendidikan = request.POST["nomor_seri_ijazah_pendidikan"]
        tanggal_terbit_ijazah_pendidikan = request.POST[
            "tanggal_terbit_ijazah_pendidikan"
        ]
        file_ijazah_pendidikan = request.FILES["file_ijazah_pendidikan"]

        # Validasi tipe file
        if not file_ijazah_pendidikan.name.endswith(".pdf"):
            messages.error(request, "File harus berformat PDF.")
            return redirect("profile")

        # Validasi ukuran file
        max_size = 500 * 1024  # 500KB
        if file_ijazah_pendidikan.size > max_size:
            messages.error(request, "Ukuran file melebihi 500KB.")
            return redirect("profile")

        # Dapatkan username dari pengguna yang saat ini masuk
        username = request.user.username
        # Ubah nama file yang akan diunggah
        new_file_name = f"{username}_pendidikan_{tingkat_pendidikan}{file_ijazah_pendidikan.name[file_ijazah_pendidikan.name.rfind('.'):]}"
        fs = FileSystemStorage()

        try:
            pendidikan = get_object_or_404(
                Pendidikan, id_pendidikan=id_pendidikan, user=user_id
            )
            # Hapus file dan data pendidikan sebelumnya
            if pendidikan.file_ijazah_pendidikan:
                old_file_path = pendidikan.file_ijazah_pendidikan.path
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Update data pendidikan
            pendidikan.tingkat_pendidikan = tingkat_pendidikan
            pendidikan.lembaga_pendidikan = lembaga_pendidikan
            pendidikan.fakultas_pendidikan = fakultas_pendidikan
            pendidikan.jurusan_pendidikan = jurusan_pendidikan
            pendidikan.gelar_depan_pendidikan = gelar_depan_pendidikan
            pendidikan.gelar_belakang_pendidikan = gelar_belakang_pendidikan
            pendidikan.nomor_seri_ijazah_pendidikan = nomor_seri_ijazah_pendidikan
            pendidikan.tanggal_terbit_ijazah_pendidikan = (
                tanggal_terbit_ijazah_pendidikan
            )
            pendidikan.file_ijazah_pendidikan = fs.save(
                f"media/pendidikan/{new_file_name}", file_ijazah_pendidikan
            )
            pendidikan.save()
            messages.success(request, "Data Pendidikan berhasil diubah.")
        except Pendidikan.DoesNotExist:
            messages.warning(
                request, "Data Pendidikan tidak ditemukan. Tolong gunakan fungsi buat."
            )

        return redirect("profile")

    return render(request, "pegawai/profile.html")


@login_required
def delete_pendidikan(request, id_pendidikan):
    pendidikan = get_object_or_404(
        Pendidikan, id_pendidikan=id_pendidikan, user=request.user
    )

    try:
        # Hapus file dan data pendidikan
        if pendidikan.file_ijazah_pendidikan:
            old_file_path = pendidikan.file_ijazah_pendidikan.path
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        pendidikan.delete()
        messages.success(request, "Data Pendidikan berhasil dihapus.")
    except Pendidikan.DoesNotExist:
        messages.warning(request, "Data Pendidikan tidak ditemukan.")

    return redirect("profile")


@login_required
def download_ijazah(request, id_pendidikan):
    pendidikan = get_object_or_404(Pendidikan, id_pendidikan=id_pendidikan)

    # Pastikan pengguna yang mengakses adalah pemilik data ijazah
    if pendidikan.user != request.user:
        messages.error(request, "Anda tidak memiliki izin untuk mengunduh ijazah ini.")
        return redirect("profile")

    # Cek apakah file_ijazah_pendidikan ada atau tidak
    if not pendidikan.file_ijazah_pendidikan:
        raise Http404("File Ijazah tidak ditemukan")

    # Dapatkan path lengkap ke file ijazah
    file_path = pendidikan.file_ijazah_pendidikan.path

    # Buka file sebagai binary dan kirim sebagai HTTP response
    with open(file_path, "rb") as file:
        response = HttpResponse(
            file.read(), content_type="application/pdf"
        )  # Sesuaikan content_type sesuai tipe file

        # Mengatur header untuk attachment agar file dapat diunduh
        response[
            "Content-Disposition"
        ] = f"attachment; filename={pendidikan.file_ijazah_pendidikan.name}"

        return response


##### JABATAN #####
@login_required
def add_jabatan(request):
    user_id = request.user.id

    if request.method == "POST" and request.FILES["file_sk_jabatan"]:
        nama_jabatan = request.POST["nama_jabatan"]
        nomor_sk_jabatan = request.POST["nomor_sk_jabatan"]
        tanggal_sk_jabatan = request.POST["tanggal_sk_jabatan"]
        tmt_jabatan = request.POST["tmt_jabatan"]
        file_sk_jabatan = request.FILES["file_sk_jabatan"]

        # Validasi tipe file
        if not file_sk_jabatan.name.endswith(".pdf"):
            messages.error(request, "File harus berformat PDF.")
            return redirect("profile")

        # Validasi ukuran file
        max_size = 500 * 1024  # 500KB
        if file_sk_jabatan.size > max_size:
            messages.error(request, "Ukuran file melebihi 500KB.")
            return redirect("profile")

        # Dapatkan username dari pengguna yang saat ini masuk
        username = request.user.username
        # Ubah nama file yang akan diunggah
        new_file_name = f"{username}_jabatan_{nama_jabatan}{file_sk_jabatan.name[file_sk_jabatan.name.rfind('.'):]}"
        fs = FileSystemStorage()

        try:
            Jabatan.objects.get(
                nama_jabatan=nama_jabatan,
                nomor_sk_jabatan=nomor_sk_jabatan,
                user_id=user_id,
            )
            messages.warning(
                request,
                "Data Jabatan sudah ada. Tolong gunakan fungsi edit.",
            )
            return redirect("profile")
        except Jabatan.DoesNotExist:
            Jabatan.objects.create(
                nama_jabatan=nama_jabatan,
                nomor_sk_jabatan=nomor_sk_jabatan,
                tanggal_sk_jabatan=tanggal_sk_jabatan,
                tmt_jabatan=tmt_jabatan,
                file_sk_jabatan=fs.save(
                    f"media/jabatan/{new_file_name}", file_sk_jabatan
                ),
                user_id=user_id,
            )
            messages.success(request, "Data Jabatan berhasil dibuat.")
            return redirect("profile")

    return render(request, "pegawai/profile.html")


@login_required
def edit_jabatan(request, id_jabatan):
    user_id = request.user.id

    if request.method == "POST" and request.FILES["file_sk_jabatan"]:
        nama_jabatan = request.POST["nama_jabatan"]
        nomor_sk_jabatan = request.POST["nomor_sk_jabatan"]
        tanggal_sk_jabatan = request.POST["tanggal_sk_jabatan"]
        tmt_jabatan = request.POST["tmt_jabatan"]
        file_sk_jabatan = request.FILES["file_sk_jabatan"]

        # Validasi tipe file
        if not file_sk_jabatan.name.endswith(".pdf"):
            messages.error(request, "File harus berformat PDF.")
            return redirect("profile")

        # Validasi ukuran file
        max_size = 500 * 1024  # 500KB
        if file_sk_jabatan.size > max_size:
            messages.error(request, "Ukuran file melebihi 500KB.")
            return redirect("profile")

        # Dapatkan username dari pengguna yang saat ini masuk
        username = request.user.username
        # Ubah nama file yang akan diunggah
        new_file_name = f"{username}_jabatan_{nama_jabatan}{file_sk_jabatan.name[file_sk_jabatan.name.rfind('.'):]}"
        fs = FileSystemStorage()

        try:
            jabatan = get_object_or_404(Jabatan, id_jabatan=id_jabatan, user=user_id)
            # Hapus file dan data jabatan sebelumnya
            if jabatan.file_sk_jabatan:
                old_file_path = jabatan.file_sk_jabatan.path
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Update data jabatan
            jabatan.nama_jabatan = nama_jabatan
            jabatan.nomor_sk_jabatan = nomor_sk_jabatan
            jabatan.tanggal_sk_jabatan = tanggal_sk_jabatan
            jabatan.tmt_jabatan = tmt_jabatan
            jabatan.file_sk_jabatan = fs.save(
                f"media/jabatan/{new_file_name}", file_sk_jabatan
            )
            jabatan.save()
            messages.success(request, "Data Jabatan berhasil diubah.")
        except Jabatan.DoesNotExist:
            messages.warning(
                request, "Data Jabatan tidak ditemukan. Tolong gunakan fungsi buat."
            )

        return redirect("profile")

    return render(request, "pegawai/profile.html")


@login_required
def delete_jabatan(request, id_jabatan):
    jabatan = get_object_or_404(Jabatan, id_jabatan=id_jabatan, user=request.user)

    try:
        # Hapus file dan data jabatan
        if jabatan.file_sk_jabatan:
            old_file_path = jabatan.file_sk_jabatan.path
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        jabatan.delete()
        messages.success(request, "Data Jabatan berhasil dihapus.")
    except Jabatan.DoesNotExist:
        messages.warning(request, "Data Jabatan tidak ditemukan.")

    return redirect("profile")


@login_required
def download_sk_jabatan(request, id_jabatan):
    jabatan = get_object_or_404(Jabatan, id_jabatan=id_jabatan)

    # Pastikan pengguna yang mengakses adalah pemilik data SK
    if jabatan.user != request.user:
        messages.error(request, "Anda tidak memiliki izin untuk mengunduh SK ini.")
        return redirect("profile")

    # Cek apakah file_sk_jabatan ada atau tidak
    if not jabatan.file_sk_jabatan:
        raise Http404("File SK tidak ditemukan")

    # Dapatkan path lengkap ke file SK
    file_path = jabatan.file_sk_jabatan.path

    # Buka file sebagai binary dan kirim sebagai HTTP response
    with open(file_path, "rb") as file:
        response = HttpResponse(
            file.read(), content_type="application/pdf"
        )  # Sesuaikan content_type sesuai tipe file

        # Mengatur header untuk attachment agar file dapat diunduh
        response[
            "Content-Disposition"
        ] = f"attachment; filename={jabatan.file_sk_jabatan.name}"

        return response


##### PANGKAT DAN GOLONGAN #####
@login_required
def add_pangkat(request):
    user_id = request.user.id

    if request.method == "POST" and request.FILES["file_sk_pangkat"]:
        nama_pangkat = request.POST["nama_pangkat"]
        nomor_sk_pangkat = request.POST["nomor_sk_pangkat"]
        tanggal_sk_pangkat = request.POST["tanggal_sk_pangkat"]
        tmt_pangkat = request.POST["tmt_pangkat"]
        file_sk_pangkat = request.FILES["file_sk_pangkat"]

        # Validasi tipe file
        if not file_sk_pangkat.name.endswith(".pdf"):
            messages.error(request, "File harus berformat PDF.")
            return redirect("profile")

        # Validasi ukuran file
        max_size = 500 * 1024  # 500KB
        if file_sk_pangkat.size > max_size:
            messages.error(request, "Ukuran file melebihi 500KB.")
            return redirect("profile")

        # Dapatkan username dari pengguna yang saat ini masuk
        username = request.user.username
        # Ubah nama file yang akan diunggah
        new_file_name = f"{username}_pangkat_{nama_pangkat}{file_sk_pangkat.name[file_sk_pangkat.name.rfind('.'):]}"
        fs = FileSystemStorage()

        try:
            Pangkat.objects.get(
                nama_pangkat=nama_pangkat,
                nomor_sk_pangkat=nomor_sk_pangkat,
                user_id=user_id,
            )
            messages.warning(
                request,
                "Data Pangkat dan Golongan sudah ada. Tolong gunakan fungsi edit.",
            )
            return redirect("profile")
        except Pangkat.DoesNotExist:
            Pangkat.objects.create(
                nama_pangkat=nama_pangkat,
                nomor_sk_pangkat=nomor_sk_pangkat,
                tanggal_sk_pangkat=tanggal_sk_pangkat,
                tmt_pangkat=tmt_pangkat,
                file_sk_pangkat=fs.save(
                    f"media/pangkat/{new_file_name}", file_sk_pangkat
                ),
                user_id=user_id,
            )
            messages.success(request, "Data Pangkat berhasil dibuat.")
            return redirect("profile")

    return render(request, "pegawai/profile.html")


@login_required
def edit_pangkat(request, id_pangkat):
    user_id = request.user.id

    if request.method == "POST" and request.FILES["file_sk_pangkat"]:
        nama_pangkat = request.POST["nama_pangkat"]
        nomor_sk_pangkat = request.POST["nomor_sk_pangkat"]
        tanggal_sk_pangkat = request.POST["tanggal_sk_pangkat"]
        tmt_pangkat = request.POST["tmt_pangkat"]
        file_sk_pangkat = request.FILES["file_sk_pangkat"]

        # Validasi tipe file
        if not file_sk_pangkat.name.endswith(".pdf"):
            messages.error(request, "File harus berformat PDF.")
            return redirect("profile")

        # Validasi ukuran file
        max_size = 500 * 1024  # 500KB
        if file_sk_pangkat.size > max_size:
            messages.error(request, "Ukuran file melebihi 500KB.")
            return redirect("profile")

        # Dapatkan username dari pengguna yang saat ini masuk
        username = request.user.username
        # Ubah nama file yang akan diunggah
        new_file_name = f"{username}_pangkat_{nama_pangkat}{file_sk_pangkat.name[file_sk_pangkat.name.rfind('.'):]}"
        fs = FileSystemStorage()

        try:
            pangkat = get_object_or_404(Pangkat, id_pangkat=id_pangkat, user=user_id)
            # Hapus file dan data pangkat sebelumnya
            if pangkat.file_sk_pangkat:
                old_file_path = pangkat.file_sk_pangkat.path
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Update data pangkat
            pangkat.nama_pangkat = nama_pangkat
            pangkat.nomor_sk_pangkat = nomor_sk_pangkat
            pangkat.tanggal_sk_pangkat = tanggal_sk_pangkat
            pangkat.tmt_pangkat = tmt_pangkat
            pangkat.file_sk_pangkat = fs.save(
                f"media/pangkat/{new_file_name}", file_sk_pangkat
            )
            pangkat.save()
            messages.success(request, "Data Pangkat dan Golongan berhasil diubah.")
        except Pangkat.DoesNotExist:
            messages.warning(
                request, "Data Pangkat tidak ditemukan. Tolong gunakan fungsi buat."
            )

        return redirect("profile")

    return render(request, "pegawai/profile.html")


@login_required
def delete_pangkat(request, id_pangkat):
    pangkat = get_object_or_404(Pangkat, id_pangkat=id_pangkat, user=request.user)

    try:
        # Hapus file dan data pangkat
        if pangkat.file_sk_pangkat:
            old_file_path = pangkat.file_sk_pangkat.path
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        pangkat.delete()
        messages.success(request, "Data Pangkat dan Golongan berhasil dihapus.")
    except Pangkat.DoesNotExist:
        messages.warning(request, "Data Pangkat dan Golongan tidak ditemukan.")

    return redirect("profile")


@login_required
def download_sk_pangkat(request, id_pangkat):
    pangkat = get_object_or_404(Pangkat, id_pangkat=id_pangkat)

    # Pastikan pengguna yang mengakses adalah pemilik data SK
    if pangkat.user != request.user:
        messages.error(request, "Anda tidak memiliki izin untuk mengunduh SK ini.")
        return redirect("profile")

    # Cek apakah file_sk_pangkat ada atau tidak
    if not pangkat.file_sk_pangkat:
        raise Http404("File SK tidak ditemukan")

    # Dapatkan path lengkap ke file SK
    file_path = pangkat.file_sk_pangkat.path

    # Buka file sebagai binary dan kirim sebagai HTTP response
    with open(file_path, "rb") as file:
        response = HttpResponse(
            file.read(), content_type="application/pdf"
        )  # Sesuaikan content_type sesuai tipe file

        # Mengatur header untuk attachment agar file dapat diunduh
        response[
            "Content-Disposition"
        ] = f"attachment; filename={pangkat.file_sk_pangkat.name}"

        return response


##### PENILAIAN ANGKA KREDIT (PAK) #####
@login_required
def add_pak(request):
    user_id = request.user.id

    if request.method == "POST" and request.FILES["file_pak"]:
        nomor_pak = request.POST["nomor_pak"]
        tanggal_pak = request.POST["tanggal_pak"]
        nilai_pak = request.POST["nilai_pak"]
        masa_penilaian_pak = request.POST["masa_penilaian_pak"]
        file_pak = request.FILES["file_pak"]

        # Validasi tipe file
        if not file_pak.name.endswith(".pdf"):
            messages.error(request, "File harus berformat PDF.")
            return redirect("profile")

        # Validasi ukuran file
        max_size = 500 * 1024  # 500KB
        if file_pak.size > max_size:
            messages.error(request, "Ukuran file melebihi 500KB.")
            return redirect("profile")

        # Dapatkan username dari pengguna yang saat ini masuk
        username = request.user.username
        # Ubah nama file yang akan diunggah
        new_file_name = (
            f"{username}_pak_{nomor_pak}{file_pak.name[file_pak.name.rfind('.'):]}"
        )
        fs = FileSystemStorage()

        try:
            AngkaKredit.objects.get(
                nomor_pak=nomor_pak,
                tanggal_pak=tanggal_pak,
                user_id=user_id,
            )
            messages.warning(
                request,
                "Data PAK sudah ada. Tolong gunakan fungsi edit.",
            )
            return redirect("profile")
        except AngkaKredit.DoesNotExist:
            AngkaKredit.objects.create(
                nomor_pak=nomor_pak,
                tanggal_pak=tanggal_pak,
                nilai_pak=nilai_pak,
                masa_penilaian_pak=masa_penilaian_pak,
                file_pak=fs.save(f"media/angkaKredit/{new_file_name}", file_pak),
                user_id=user_id,
            )
            messages.success(request, "Data PAK berhasil dibuat.")
            return redirect("profile")

    return render(request, "pegawai/profile.html")


@login_required
def edit_pak(request, id_pak):
    user_id = request.user.id

    if request.method == "POST" and request.FILES["file_pak"]:
        nomor_pak = request.POST["nomor_pak"]
        tanggal_pak = request.POST["tanggal_pak"]
        nilai_pak = request.POST["nilai_pak"]
        masa_penilaian_pak = request.POST["masa_penilaian_pak"]
        file_pak = request.FILES["file_pak"]

        # Validasi tipe file
        if not file_pak.name.endswith(".pdf"):
            messages.error(request, "File harus berformat PDF.")
            return redirect("profile")

        # Validasi ukuran file
        max_size = 500 * 1024  # 500KB
        if file_pak.size > max_size:
            messages.error(request, "Ukuran file melebihi 500KB.")
            return redirect("profile")

        # Dapatkan username dari pengguna yang saat ini masuk
        username = request.user.username
        # Ubah nama file yang akan diunggah
        new_file_name = (
            f"{username}_pak_{nomor_pak}{file_pak.name[file_pak.name.rfind('.'):]}"
        )
        fs = FileSystemStorage()

        try:
            pak = get_object_or_404(AngkaKredit, id_pak=id_pak, user=user_id)
            # Hapus file dan data PAK sebelumnya
            if pak.file_pak:
                old_file_path = pak.file_pak.path
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Update data PAK
            pak.nomor_pak = nomor_pak
            pak.tanggal_pak = tanggal_pak
            pak.nilai_pak = nilai_pak
            pak.masa_penilaian_pak = masa_penilaian_pak
            pak.file_pak = fs.save(f"media/angkaKredit/{new_file_name}", file_pak)
            pak.save()
            messages.success(request, "Data PAK berhasil diubah.")
        except AngkaKredit.DoesNotExist:
            messages.warning(
                request, "Data PAK tidak ditemukan. Tolong gunakan fungsi buat."
            )

        return redirect("profile")

    return render(request, "pegawai/profile.html")


@login_required
def delete_pak(request, id_pak):
    pak = get_object_or_404(AngkaKredit, id_pak=id_pak, user=request.user)

    try:
        # Hapus file dan data PAK
        if pak.file_pak:
            old_file_path = pak.file_pak.path
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        pak.delete()
        messages.success(request, "Data PAK berhasil dihapus.")
    except AngkaKredit.DoesNotExist:
        messages.warning(request, "Data PAK tidak ditemukan.")

    return redirect("profile")


@login_required
def download_file_pak(request, id_pak):
    pak = get_object_or_404(AngkaKredit, id_pak=id_pak)

    # Pastikan pengguna yang mengakses adalah pemilik data File
    if pak.user != request.user:
        messages.error(request, "Anda tidak memiliki izin untuk mengunduh File ini.")
        return redirect("profile")

    # Cek apakah file_pak ada atau tidak
    if not pak.file_pak:
        raise Http404("File SK tidak ditemukan")

    # Dapatkan path lengkap ke file PAK
    file_path = pak.file_pak.path

    # Buka file sebagai binary dan kirim sebagai HTTP response
    with open(file_path, "rb") as file:
        response = HttpResponse(
            file.read(), content_type="application/pdf"
        )  # Sesuaikan content_type sesuai tipe file

        # Mengatur header untuk attachment agar file dapat diunduh
        response["Content-Disposition"] = f"attachment; filename={pak.file_pak.name}"

        return response


##### DIKLAT #####
@login_required
def add_diklat(request):
    user_id = request.user.id

    if request.method == "POST" and request.FILES["file_sertifikat_diklat"]:
        nama_diklat = request.POST["nama_diklat"]
        tanggal_mulai_diklat = request.POST["tanggal_mulai_diklat"]
        tanggal_selesai_diklat = request.POST["tanggal_selesai_diklat"]
        nomor_sertifikat_diklat = request.POST["nomor_sertifikat_diklat"]
        tanggal_sertifikat_diklat = request.POST["tanggal_sertifikat_diklat"]
        file_sertifikat_diklat = request.FILES["file_sertifikat_diklat"]

        # Validasi tipe file
        if not file_sertifikat_diklat.name.endswith(".pdf"):
            messages.error(request, "File harus berformat PDF.")
            return redirect("profile")

        # Validasi ukuran file
        max_size = 500 * 1024  # 500KB
        if file_sertifikat_diklat.size > max_size:
            messages.error(request, "Ukuran file melebihi 500KB.")
            return redirect("profile")

        # Dapatkan username dari pengguna yang saat ini masuk
        username = request.user.username
        # Ubah nama file yang akan diunggah
        new_file_name = f"{username}_diklat_{nomor_sertifikat_diklat}{file_sertifikat_diklat.name[file_sertifikat_diklat.name.rfind('.'):]}"
        fs = FileSystemStorage()

        try:
            Diklat.objects.get(
                nomor_sertifikat_diklat=nomor_sertifikat_diklat,
                tanggal_sertifikat_diklat=tanggal_sertifikat_diklat,
                user_id=user_id,
            )
            messages.warning(
                request,
                "Data Diklat sudah ada. Tolong gunakan fungsi edit.",
            )
            return redirect("profile")
        except Diklat.DoesNotExist:
            Diklat.objects.create(
                nama_diklat=nama_diklat,
                tanggal_mulai_diklat=tanggal_mulai_diklat,
                tanggal_selesai_diklat=tanggal_selesai_diklat,
                nomor_sertifikat_diklat=nomor_sertifikat_diklat,
                tanggal_sertifikat_diklat=tanggal_sertifikat_diklat,
                file_sertifikat_diklat=fs.save(
                    f"media/diklat/{new_file_name}", file_sertifikat_diklat
                ),
                user_id=user_id,
            )
            messages.success(request, "Data Diklat berhasil dibuat.")
            return redirect("profile")

    return render(request, "pegawai/profile.html")


@login_required
def edit_diklat(request, id_diklat):
    user_id = request.user.id

    if request.method == "POST" and request.FILES["file_sertifikat_diklat"]:
        nama_diklat = request.POST["nama_diklat"]
        tanggal_mulai_diklat = request.POST["tanggal_mulai_diklat"]
        tanggal_selesai_diklat = request.POST["tanggal_selesai_diklat"]
        nomor_sertifikat_diklat = request.POST["nomor_sertifikat_diklat"]
        tanggal_sertifikat_diklat = request.POST["tanggal_sertifikat_diklat"]
        file_sertifikat_diklat = request.FILES["file_sertifikat_diklat"]

        # Validasi tipe file
        if not file_sertifikat_diklat.name.endswith(".pdf"):
            messages.error(request, "File harus berformat PDF.")
            return redirect("profile")

        # Validasi ukuran file
        max_size = 500 * 1024  # 500KB
        if file_sertifikat_diklat.size > max_size:
            messages.error(request, "Ukuran file melebihi 500KB.")
            return redirect("profile")

        # Dapatkan username dari pengguna yang saat ini masuk
        username = request.user.username
        # Ubah nama file yang akan diunggah
        new_file_name = f"{username}_diklat_{nomor_sertifikat_diklat}{file_sertifikat_diklat.name[file_sertifikat_diklat.name.rfind('.'):]}"
        fs = FileSystemStorage()

        try:
            diklat = get_object_or_404(Diklat, id_diklat=id_diklat, user=user_id)
            # Hapus file dan data Diklat sebelumnya
            if diklat.file_sertifikat_diklat:
                old_file_path = diklat.file_sertifikat_diklat.path
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Update data Diklat
            diklat.nama_diklat = nama_diklat
            diklat.tanggal_mulai_diklat = tanggal_mulai_diklat
            diklat.tanggal_selesai_diklat = tanggal_selesai_diklat
            diklat.nomor_sertifikat_diklat = nomor_sertifikat_diklat
            diklat.tanggal_sertifikat_diklat = tanggal_sertifikat_diklat
            diklat.file_sertifikat_diklat = fs.save(
                f"media/diklat/{new_file_name}", file_sertifikat_diklat
            )
            diklat.save()
            messages.success(request, "Data Diklat berhasil diubah.")
        except Diklat.DoesNotExist:
            messages.warning(
                request, "Data Diklat tidak ditemukan. Tolong gunakan fungsi buat."
            )

        return redirect("profile")

    return render(request, "pegawai/profile.html")


@login_required
def delete_diklat(request, id_diklat):
    diklat = get_object_or_404(Diklat, id_diklat=id_diklat, user=request.user)

    try:
        # Hapus file dan data Diklat
        if diklat.file_sertifikat_diklat:
            old_file_path = diklat.file_sertifikat_diklat.path
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        diklat.delete()
        messages.success(request, "Data Diklat berhasil dihapus.")
    except Diklat.DoesNotExist:
        messages.warning(request, "Data Diklat tidak ditemukan.")

    return redirect("profile")


@login_required
def download_file_diklat(request, id_diklat):
    diklat = get_object_or_404(Diklat, id_diklat=id_diklat)

    # Pastikan pengguna yang mengakses adalah pemilik data File
    if diklat.user != request.user:
        messages.error(request, "Anda tidak memiliki izin untuk mengunduh File ini.")
        return redirect("profile")

    # Cek apakah file_sertifikat_diklat ada atau tidak
    if not diklat.file_sertifikat_diklat:
        raise Http404("File Sertifikat tidak ditemukan")

    # Dapatkan path lengkap ke file Diklat
    file_path = diklat.file_sertifikat_diklat.path

    # Buka file sebagai binary dan kirim sebagai HTTP response
    with open(file_path, "rb") as file:
        response = HttpResponse(
            file.read(), content_type="application/pdf"
        )  # Sesuaikan content_type sesuai tipe file

        # Mengatur header untuk attachment agar file dapat diunduh
        response[
            "Content-Disposition"
        ] = f"attachment; filename={diklat.file_sertifikat_diklat.name}"

        return response
