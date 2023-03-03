from django.contrib import admin
from tasks.models import Data
from tasks.models import Credit
# Register your models here.

admin.site.register(Data)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('user', 'value')  # Campos que se mostrarán en la lista de objetos

admin.site.register(Credit, CreditAdmin)  # Registrar el modelo Credit en el panel de administrador