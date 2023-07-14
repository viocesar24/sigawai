from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings


class Pegawai(models.Model):
    id_pegawai = models.AutoField(primary_key=True)
    nip_pegawai = models.IntegerField(unique=True, default=0)
    nama_pegawai = models.CharField(blank=False, max_length=200)
    tempat_lahir_pegawai = models.CharField(blank=False, max_length=200)
    tanggal_lahir_pegawai = models.DateField(blank=False)

    class JenisKelamin(models.TextChoices):
        MALE = "Laki-Laki", _("Laki-Laki")
        FEMALE = "Perempuan", _("Perempuan")

    jenis_kelamin_pegawai = models.CharField(
        blank=False, max_length=200, choices=JenisKelamin.choices
    )
    surel_pegawai = models.EmailField(blank=False, max_length=200)
    telepon_pegawai = models.CharField(blank=False, max_length=200)
    aktif_pegawai = models.BooleanField(blank=False, default=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, default=None
    )


def pegawai_jalur_direktori(instance, filename):
    # file akan diunggah ke MEDIA_ROOT/pegawai_id_pegawai/<namaFile>
    return "pegawai_{0}/{1}".format(instance.pegawai.id_pegawai, filename)


class Jabatan(models.Model):
    id_jabatan = models.AutoField(primary_key=True)

    class NamaJabatan(models.TextChoices):
        INSP = "1", _("Inspektur")
        SEKRE = "2", _("Sekretaris Inspektorat")
        SUBUM = "3", _("Kepala Sub Bagian Administrasi dan Umum")
        IRBANI = "4", _("Inspektur Pembantu I")
        IRBANII = "5", _("Inspektur Pembantu II")
        IRBANIII = "6", _("Inspektur Pembantu III")
        IRBANIV = "7", _("Inspektur Pembantu IV")
        IRBANSUS = "8", _("Inspektur Pembantu Khusus")
        JFAUPEL = "9", _("JF Auditor Pelaksana")
        JFAUPELAN = "10", _("JF Auditor Pelaksana Lanjutan")
        JFAUPEN = "11", _("JF Auditor Penyelia")
        JFAUPER = "12", _("JF Auditor Pertama")
        JFAUMAD = "13", _("JF Auditor Madya")
        JFAUUT = "14", _("JF Auditor Utama")
        JFPPUPDP = "15", _(
            "JF Pengawas Penyelenggaraan Urusan Pemerintahan Daerah Pertama"
        )
        JFPPUPDMU = "16", _(
            "JF Pengawas Penyelenggaraan Urusan Pemerintahan Daerah Muda"
        )
        JFPPUPDMA = "17", _(
            "JF Pengawas Penyelenggaraan Urusan Pemerintahan Daerah Madya"
        )
        JFAUKEPER = "18", _("JF Auditor Kepegawaian Pertama")
        JFAUKEMU = "19", _("JF Auditor Kepegawaian Muda")
        JFAUKEMA = "20", _("JF Auditor Kepegawaian Madya")
        JFAKPPER = "21", _("JF Analis Keuangan Pusat dan Daerah Ahli Pertama")
        JFAKPMU = "22", _("JF Analis Keuangan Pusat dan Daerah Ahli Muda")
        JFAKPMA = "23", _("JF Analis Keuangan Pusat dan Daerah Ahli Madya")
        JFPERAPER = "24", _("JF Perencana Ahli Pertama")
        JFPERAMU = "25", _("JF Perencana Ahli Muda")
        JFPERAMA = "26", _("JF Perencana Ahli Madya")
        JFPELABATE = "27", _("JF Penata Laksana Barang Terampil")
        JFPELABAMA = "28", _("JF Penata Laksana Barang Mahir")
        JFPELABAPE = "29", _("JF Penata Laksana Barang Penyelia")
        ATLLHP = "30", _("Analis Tindak Lanjut Laporan Hasil Pemeriksaan")
        APIP = "31", _("Analis Pengawasan Intern Pemerintah")
        AHPPM = "32", _("Analis Hasil Pengawasan dan Pengaduan Masyarakat")
        PDLP = "33", _("Pengelola Data Laporan dan Pengaduan")
        PLHPKN = "34", _("Penelaah Laporan Hasil Pemeriksaan dan Kerugian Negara")
        PRKSP = "35", _("Penyusun Rencana Kebutuhan Sarana dan Prasarana")
        PSPK = "36", _("Pengelola Sarana dan Prasarana Kantor")
        PSIMK = "37", _("Pengelola Sistem Informasi Manajemen Kepegawaian")
        PEUM = "38", _("Pengadministrasi Umum")
        PMUDI = "39", _("Pengemudi")
        PAMAN = "40", _("Petugas Keamanan")
        PIHAN = "41", _("Pramu Kebersihan")
        BENDA = "42", _("Bendahara")
        PLKEU = "43", _("Penata Laporan Keuangan")
        PKEU = "44", _("Pengelola Keuangan")
        PPKIN = "45", _("Pengevaluasi Program dan Kinerja")
        PRKAN = "46", _("Penyusun Rencana Kegiatan dan Anggaran")
        PMDEV = "47", _("Pengelola Monitoring dan Evaluasi")
        PPPRO = "48", _("Pengadministrasi Perencanaan dan Program")

    nama_jabatan = models.CharField(
        blank=False,
        max_length=2,
        choices=NamaJabatan.choices,
    )
    nomor_sk_jabatan = models.CharField(blank=False, max_length=200)
    tanggal_sk_jabatan = models.DateField(blank=False)
    tmt_jabatan = models.CharField(blank=False, max_length=200)
    file_sk_jabatan = models.FileField(upload_to=pegawai_jalur_direktori)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, default=None
    )


class Pendidikan(models.Model):
    id_pendidikan = models.AutoField(primary_key=True)

    class TingkatPendidikan(models.TextChoices):
        SD = "SD", _("Sekolah Dasar")
        SMP = "SMP", _("Sekolah Menengah Pertama")
        SMA = "SMA", _("Sekolah Menengah Atas")
        D1 = "D1", _("Diploma Satu")
        D2 = "D2", _("Diploma Dua")
        D3 = "D3", _("Diploma Tiga")
        D4 = "D4", _("Diploma Empat")
        S1 = "S1", _("Sarjana Satu")
        S2 = "S2", _("Sarjana Dua")
        S3 = "S3", _("Sarjana Tiga")

    tingkat_pendidikan = models.CharField(
        blank=False,
        max_length=3,
        choices=TingkatPendidikan.choices,
        default=TingkatPendidikan.SD,
    )
    lembaga_pendidikan = models.CharField(blank=False, max_length=200)
    fakultas_pendidikan = models.CharField(blank=False, max_length=200)
    jurusan_pendidikan = models.CharField(blank=False, max_length=200)
    gelar_depan_pendidikan = models.CharField(blank=False, max_length=100)
    gelar_belakang_pendidikan = models.CharField(blank=False, max_length=100)
    nomor_seri_ijazah_pendidikan = models.CharField(blank=False, max_length=200)
    tanggal_terbit_ijazah_pendidikan = models.DateField(blank=False)
    file_ijazah_pendidikan = models.FileField(upload_to=pegawai_jalur_direktori)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, default=None
    )


class Pangkat(models.Model):
    id_pangkat = models.AutoField(primary_key=True)

    class KodePangkat(models.TextChoices):
        IA = "IA", _("Juru Muda")
        IB = "IB", _("Juru Muda Tingkat 1")
        IC = "IC", _("Juru")
        ID = "ID", _("Juru Tingkat 1")
        IIA = "IIA", _("Pengatur Muda")
        IIB = "IIB", _("Pengatur Muda Tingkat 1")
        IIC = "IIC", _("Pengatur")
        IID = "IID", _("Pengatur Tingkat 1")
        IIIA = "IIIA", _("Penata Muda")
        IIIB = "IIIB", _("Penata Muda Tingkat 1")
        IIIC = "IIIC", _("Penata")
        IIID = "IIID", _("Penata Tingkat 1")
        IVA = "IVA", _("Pembina")
        IVB = "IVB", _("Pembina Tingkat 1")
        IVC = "IVC", _("Pembina Utama Muda")
        IVD = "IVD", _("Pembina Utama Madya")
        IVE = "IVE", _("Pembina Utama")

    nama_pangkat = models.CharField(
        max_length=4,
        choices=KodePangkat.choices,
        default=KodePangkat.IA,
    )
    golongan_ruang_pangkat = models.CharField(blank=False, max_length=200)
    nomor_sk_pangkat = models.CharField(blank=False, max_length=200)
    tanggal_sk_pangkat = models.DateField(blank=False)
    tmt_pangkat = models.CharField(blank=False, max_length=200)
    file_sk_pangkat = models.FileField(upload_to=pegawai_jalur_direktori)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, default=None
    )


class Diklat(models.Model):
    id_diklat = models.AutoField(primary_key=True)
    nama_diklat = models.CharField(blank=False, max_length=200)
    tanggal_mulai_diklat = models.DateField(blank=True)
    tanggal_selesai_diklat = models.DateField(blank=True)
    nomor_sertifikat_diklat = models.CharField(blank=False, max_length=200)
    tanggal_sertifikat_diklat = models.DateField(blank=False)
    file_sertifikat_diklat = models.FileField(upload_to=pegawai_jalur_direktori)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, default=None
    )


class AngkaKredit(models.Model):
    id_pak = models.AutoField(primary_key=True)
    nomor_pak = models.CharField(blank=False, max_length=200)
    tanggal_pak = models.DateField(blank=False)
    nilai_pak = models.IntegerField(blank=False)

    class MasaPenilaian(models.TextChoices):
        SEM1 = "Semester Ganjil", _("Semester Ganjil")
        SEM2 = "Semester Genap", _("Semester Genap")

    masa_penilaian_pak = models.CharField(
        blank=False, max_length=200, choices=MasaPenilaian.choices
    )
    file_pak = models.FileField(upload_to=pegawai_jalur_direktori)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, default=None
    )
