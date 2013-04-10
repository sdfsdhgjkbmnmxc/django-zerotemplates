from django.contrib import admin
from zerotemplates.models import ZeroTemplate


class ZeroTemplateAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'filename',
        'path',
        'comments',
    )

admin.site.register(ZeroTemplate, ZeroTemplateAdmin)