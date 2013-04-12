from django.contrib import admin
from django.forms import Textarea
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
            # 'widget': Textarea(attrs={'cols': 100, 'rows': 30}),
        },
    }


admin.site.register(ZeroTemplate, ZeroTemplateAdmin)
