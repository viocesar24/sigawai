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
        JFAMUDA = "14", _("JF Auditor Muda")
        JFAUUT = "15", _("JF Auditor Utama")
        JFPPUPDP = "16", _(
            "JF Pengawas Penyelenggaraan Urusan Pemerintahan Daerah Pertama"
        )
        JFPPUPDMU = "17", _(
            "JF Pengawas Penyelenggaraan Urusan Pemerintahan Daerah Muda"
        )
        JFPPUPDMA = "18", _(
            "JF Pengawas Penyelenggaraan Urusan Pemerintahan Daerah Madya"
        )
        JFAUKEPER = "19", _("JF Auditor Kepegawaian Pertama")
        JFAUKEMU = "20", _("JF Auditor Kepegawaian Muda")
        JFAUKEMA = "21", _("JF Auditor Kepegawaian Madya")
        JFAKPPER = "22", _("JF Analis Keuangan Pusat dan Daerah Ahli Pertama")
        JFAKPMU = "23", _("JF Analis Keuangan Pusat dan Daerah Ahli Muda")
        JFAKPMA = "24", _("JF Analis Keuangan Pusat dan Daerah Ahli Madya")
        JFPERAPER = "25", _("JF Perencana Ahli Pertama")
        JFPERAMU = "26", _("JF Perencana Ahli Muda")
        JFPERAMA = "27", _("JF Perencana Ahli Madya")
        JFPELABATE = "28", _("JF Penata Laksana Barang Terampil")
        JFPELABAMA = "29", _("JF Penata Laksana Barang Mahir")
        JFPELABAPE = "30", _("JF Penata Laksana Barang Penyelia")
        ATLLHP = "31", _("Analis Tindak Lanjut Laporan Hasil Pemeriksaan")
        APIP = "32", _("Analis Pengawasan Intern Pemerintah")
        AHPPM = "33", _("Analis Hasil Pengawasan dan Pengaduan Masyarakat")
        PDLP = "34", _("Pengelola Data Laporan dan Pengaduan")
        PLHPKN = "35", _("Penelaah Laporan Hasil Pemeriksaan dan Kerugian Negara")
        PRKSP = "36", _("Penyusun Rencana Kebutuhan Sarana dan Prasarana")
        PSPK = "37", _("Pengelola Sarana dan Prasarana Kantor")
        PSIMK = "38", _("Pengelola Sistem Informasi Manajemen Kepegawaian")
        PEUM = "39", _("Pengadministrasi Umum")
        PMUDI = "40", _("Pengemudi")
        PAMAN = "41", _("Petugas Keamanan")
        PIHAN = "42", _("Pramu Kebersihan")
        BENDA = "43", _("Bendahara")
        PLKEU = "44", _("Penata Laporan Keuangan")
        PKEU = "45", _("Pengelola Keuangan")
        PPKIN = "46", _("Pengevaluasi Program dan Kinerja")
        PRKAN = "47", _("Penyusun Rencana Kegiatan dan Anggaran")
        PMDEV = "48", _("Pengelola Monitoring dan Evaluasi")
        PPPRO = "49", _("Pengadministrasi Perencanaan dan Program")

    nama_jabatan = models.CharField(
        blank=False,
        max_length=2,
        choices=NamaJabatan.choices,
    )
    nomor_sk_jabatan = models.CharField(blank=False, max_length=200)
    tanggal_sk_jabatan = models.DateField(blank=False)
    tmt_jabatan = models.DateField(blank=False)
    file_sk_jabatan = models.FileField(upload_to="media/jabatan/")
    user = models.ForeignKey(
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
    fakultas_pendidikan = models.CharField(blank=True, max_length=200)
    jurusan_pendidikan = models.CharField(blank=True, max_length=200)
    gelar_depan_pendidikan = models.CharField(blank=True, max_length=100)
    gelar_belakang_pendidikan = models.CharField(blank=True, max_length=100)
    nomor_seri_ijazah_pendidikan = models.CharField(blank=False, max_length=200)
    tanggal_terbit_ijazah_pendidikan = models.DateField(blank=False)
    file_ijazah_pendidikan = models.FileField(upload_to="media/pendidikan/")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, default=None
    )


class Pangkat(models.Model):
    id_pangkat = models.AutoField(primary_key=True)

    class KodePangkat(models.TextChoices):
        IA = "Ia", _("Juru Muda")
        IB = "Ib", _("Juru Muda Tingkat 1")
        IC = "Ic", _("Juru")
        ID = "Id", _("Juru Tingkat 1")
        IIA = "IIa", _("Pengatur Muda")
        IIB = "IIb", _("Pengatur Muda Tingkat 1")
        IIC = "IIc", _("Pengatur")
        IID = "IId", _("Pengatur Tingkat 1")
        IIIA = "IIIa", _("Penata Muda")
        IIIB = "IIIb", _("Penata Muda Tingkat 1")
        IIIC = "IIIc", _("Penata")
        IIID = "IIId", _("Penata Tingkat 1")
        IVA = "IVa", _("Pembina")
        IVB = "IVb", _("Pembina Tingkat 1")
        IVC = "IVc", _("Pembina Utama Muda")
        IVD = "IVd", _("Pembina Utama Madya")
        IVE = "IVe", _("Pembina Utama")

    nama_pangkat = models.CharField(
        max_length=4,
        choices=KodePangkat.choices,
        default=KodePangkat.IA,
    )
    nomor_sk_pangkat = models.CharField(blank=False, max_length=200)
    tanggal_sk_pangkat = models.DateField(blank=False)
    tmt_pangkat = models.DateField(blank=False)
    file_sk_pangkat = models.FileField(upload_to="media/pangkat/")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, default=None
    )


class Diklat(models.Model):
    id_diklat = models.AutoField(primary_key=True)
    nama_diklat = models.CharField(blank=False, max_length=200)
    tanggal_mulai_diklat = models.DateField(blank=True)
    tanggal_selesai_diklat = models.DateField(blank=True)
    nomor_sertifikat_diklat = models.CharField(blank=False, max_length=200)
    tanggal_sertifikat_diklat = models.DateField(blank=False)
    file_sertifikat_diklat = models.FileField(upload_to="media/diklat/")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, default=None
    )


class AngkaKredit(models.Model):
    id_pak = models.AutoField(primary_key=True)
    nomor_pak = models.CharField(blank=False, max_length=200)
    tanggal_pak = models.DateField(blank=False)
    nilai_pak = models.IntegerField(blank=False)
    masa_penilaian_pak = models.DateField(blank=False)
    file_pak = models.FileField(upload_to="media/angkaKredit/")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, default=None
    )
