from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Purchase, Purchase_Confirmed, Promocodes_orders


@admin.register(Purchase)
class PurchaseAdmin(ImportExportModelAdmin):
    list_display = ("name", "status", "sum", 'number', 'quantity')


@admin.register(Purchase_Confirmed)
class PurchaseAdmin(ImportExportModelAdmin):
    list_display = ("name", "status", "sum", 'number', 'quantity')


@admin.register(Promocodes_orders)
class PurchaseAdmin(ImportExportModelAdmin):
    list_display = ("name", "data")
