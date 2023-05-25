from django.contrib import admin

# Register your models here.
from apps.producto.models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio','stock',)
    search_fields = ('nombre',)
    list_filter = ('nombre',)
