from django.conf import settings
from django.contrib import admin
from django.forms import Textarea
from django.utils.safestring import mark_safe
from django.db.models import TextField
from django.utils.translation import ugettext_lazy

from zerotemplates.models import ZeroTemplate, SpareImage


class CodeMirrorTextArea(Textarea):
    def render(self, name, value, attrs=None):
        return mark_safe(u''.join([
            super(CodeMirrorTextArea, self).render(name, value, attrs),
            u"""
                <script type="text/javascript">
                  var editor = CodeMirror.fromTextArea('id_%(name)s', {
                    path: "%(media_prefix)sjs/",
                    parserfile: "parsedjango.js",
                    stylesheet: "%(media_prefix)scss/django.css",
                    continuousScanning: 500,
                    height: "40.2em",
                    tabMode: "shift",
                    indentUnit: 4,
                    lineNumbers: false
                  });
                </script>
            """ % dict(media_prefix=settings.STATIC_URL + 'codemirror/',
                       name=name)
        ]))

    class Media:
        css = {
            'screen': ['codemirror/css/editor.css']
        }
        js = ['codemirror/js/codemirror.js']


class ImageInlineAdmin(admin.StackedInline):
    model = SpareImage
    readonly_fields = (
        'code',
    )

    def code(self, obj):
        if obj:
            return u'<img src="{0}" width="{1}" height="{2}" alt="">'.format(
                obj.image.url,
                obj.image.width,
                obj.image.height,
            )
        else:
            return ''
    code.short_description = ugettext_lazy('HTML')


class ZeroTemplateAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'filename',
        'path',
        'comments',
    )
    formfield_overrides = {
        TextField: {
            'widget': CodeMirrorTextArea(),
            # 'widget': Textarea(attrs={'cols': 100, 'rows': 30}),
        },
    }
    inlines = [
        ImageInlineAdmin,
    ]
    fieldsets = (
        (None, {
            'fields': (
                'filename',
                'comments',
                'content',
            )
        }),
        (ugettext_lazy('Render template as site page'), {
            'fields': (
                'path',
                'content_type',
            )
        }),
    )


admin.site.register(ZeroTemplate, ZeroTemplateAdmin)
