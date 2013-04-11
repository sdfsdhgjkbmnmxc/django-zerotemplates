from django.contrib import admin
from djangocodemirror.fields import CodeMirrorWidget
from django.db.models import TextField

from zerotemplates.models import ZeroTemplate


class ZeroTemplateAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'filename',
        'path',
        'comments',
    )
    formfield_overrides = {
        TextField: {
            'widget': CodeMirrorWidget(),
        },
    }


admin.site.register(ZeroTemplate, ZeroTemplateAdmin)
