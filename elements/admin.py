from django.contrib import admin

from django.contrib import messages

from .models import Element, Category, Type

# Register your models here.


from django.conf import settings


if settings.DEMO:
    class ReadOnlyAdmin(admin.ModelAdmin):
        """
        Admin que permite navegar, abrir formularios y mostrar botones,
        pero NO guarda, crea ni elimina nada en la base de datos.
        """
        def save_model(self, request, obj, form, change):
            messages.warning(
                request,
                "Este modelo es de solo lectura. Los cambios no se guardaron."
            )

        def delete_model(self, request, obj):
            messages.warning(
                request,
                "Este modelo es de solo lectura. La eliminación no se realizó."
            )

        def delete_queryset(self, request, queryset):
            messages.warning(
                request,
                "Este modelo es de solo lectura. No se eliminaron registros."
            )
    admin.site.register(Element, ReadOnlyAdmin)
    admin.site.register(Category, ReadOnlyAdmin)
    admin.site.register(Type, ReadOnlyAdmin)
else:
    admin.site.register(Element)
    admin.site.register(Category)
    admin.site.register(Type)