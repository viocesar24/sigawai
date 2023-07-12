from django.contrib import admin
from .models import Pegawai
from .models import Jabatan
from .models import Pendidikan
from .models import Pangkat
from .models import Diklat
from .models import AngkaKredit

admin.site.register(Pegawai)
admin.site.register(Jabatan)
admin.site.register(Pendidikan)
admin.site.register(Pangkat)
admin.site.register(Diklat)
admin.site.register(AngkaKredit)
