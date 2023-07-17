from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage, default_storage
from .models import Pegawai, Pendidikan
import os


def index(request):
    # Mendapatkan username user yang sedang login
    username = request.user.username
    context = {"username": username}
    return render(request, "pegawai/index.html", context)


@login_required
def profile(request):
    # Mendapatkan username user yang sedang login
    username = request.user.username

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

    # Mendapatkan data pendidikan dari user yang sedang login
    try:
        # Mengambil data tabel pendidikan
        pendidikan = Pendidikan.objects.get(user=request.user)
        # Ubah format tanggal terbit ijazah pendidikan menjadi "YYYY/MM/DD"
        tanggal_terbit_ijazah_pendidikan = (
            pendidikan.tanggal_terbit_ijazah_pendidikan.strftime("%Y-%m-%d")
        )
    except Pendidikan.DoesNotExist:
        # Jika data tabel pendidikan tidak ada maka return Null/None
        pendidikan = None
        tanggal_terbit_ijazah_pendidikan = None

    if pendidikan and pendidikan.file_ijazah_pendidikan:
        file_exists_pendidikan = default_storage.exists(
            pendidikan.file_ijazah_pendidikan.name
        )
    else:
        file_exists_pendidikan = False

    # Mengambil data pilihan tingkat pendidikan
    pilihan_tingkat_pendidikan = Pendidikan.TingkatPendidikan.choices
    context = {
        "username": username,
        "pegawai": pegawai,
        "tanggal_lahir_pegawai": tanggal_lahir_pegawai,
        "pendidikan": pendidikan,
        "tanggal_terbit_ijazah_pendidikan": tanggal_terbit_ijazah_pendidikan,
        "pilihan_tingkat_pendidikan": pilihan_tingkat_pendidikan,
        "file_exists_pendidikan": file_exists_pendidikan,
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
        # Dapatkan username dari pengguna yang saat ini masuk
        username = request.user.username
        # Ubah nama file yang akan diunggah
        new_file_name = f"{username}_pendidikan_{tingkat_pendidikan}{file_ijazah_pendidikan.name[file_ijazah_pendidikan.name.rfind('.'):]}"
        fs = FileSystemStorage()

        # Cek apakah sudah ada pendidikan dengan user_id yang sama
        try:
            pendidikan = Pendidikan.objects.get(user_id=user_id)
            # Hapus file dan data pendidikan sebelumnya
            if pendidikan.file_ijazah_pendidikan:
                old_file_path = pendidikan.file_ijazah_pendidikan.path
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            pendidikan.delete()
            pendidikan = Pendidikan.objects.get(user_id=user_id)
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
            messages.success(request, "Data pendidikan berhasil diperbarui.")
        except Pendidikan.DoesNotExist:
            # Buat pendidikan baru
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
            messages.success(request, "Pendidikan berhasil ditambahkan.")

        return redirect("profile")

    return render(request, "pegawai/profile.html")
