from django.contrib import admin

from .models import Users, Items, Staff, Promocodes

from import_export.admin import ImportExportModelAdmin


# Register your models here.
@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "yes_coin_balance", "created_at")
    readonly_fields = ("user_id",)


@admin.register(Items)
class ItemAdmin(ImportExportModelAdmin):
    list_display = ("name", "price", "category_name", "subcategory_name")


@admin.register(Staff)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("user_id", "position")


@admin.register(Promocodes)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("index", "data")
