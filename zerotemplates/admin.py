from ckeditor.widgets import CKEditorWidget, json_encode
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.db.models import TextField
from django.utils.translation import ugettext_lazy, get_language

from zerotemplates.models import ZeroTemplate, SpareImage


class CodeMirrorOrCKEditorTextArea(CKEditorWidget):
    checker = 'use_wysiwyg'

    # if value is None:
    #     value = ''
    #     final_attrs = self.build_attrs(attrs, name=name)
    #     self.config.setdefault('filebrowserUploadUrl', reverse('ckeditor_upload'))
    #     self.config.setdefault('filebrowserBrowseUrl', reverse('ckeditor_browse'))
    #     if not self.config.get('language'):
    #         self.config['language'] = get_language()
    #
    #     return mark_safe(render_to_string('ckeditor/widget.html', {
    #         'final_attrs': flatatt(final_attrs),
    #         'value': conditional_escape(force_text(value)),
    #         'id': final_attrs['id'],
    #         'config': json_encode(self.config),
    #         'external_plugin_resources' : self.external_plugin_resources
    #     }))
    # def render(self, name, value, attrs=None):
    #     # return  mark_safe(u''.join([
    #     #     super(CodeMirrorTextArea, self).render(name, value, attrs),
    #     #
    #     #     """ % dict(media_prefix=settings.STATIC_URL + 'codemirror/',
    #     #                name=name)
    #     # ]))
    #     pass

    def render(self, name, value, attrs={}):
        from django.forms.utils import flatatt
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        self.config.setdefault('filebrowserUploadUrl', reverse('ckeditor_upload'))
        self.config.setdefault('filebrowserBrowseUrl', reverse('ckeditor_browse'))
        if not self.config.get('language'):
            self.config['language'] = get_language()

        return mark_safe(render_to_string('zerotemplates/widget.html', {
            'checker': self.checker,
            'final_attrs': flatatt(final_attrs),
            'value': conditional_escape(force_text(value)),
            'id': final_attrs['id'],
            'config': json_encode(self.config),
            'external_plugin_resources': self.external_plugin_resources,
            'media_prefix': settings.STATIC_URL + 'codemirror/',
        }))

    class Media:
        js = ()
        jquery_url = getattr(settings, 'CKEDITOR_JQUERY_URL', None)
        if jquery_url:
            js += (jquery_url, )
        try:
            js += (
                settings.STATIC_URL + 'ckeditor/ckeditor/ckeditor.js',
                settings.STATIC_URL + 'ckeditor/ckeditor-init.js',
            )
        except AttributeError:
            raise ImproperlyConfigured("django-ckeditor requires \
                    CKEDITOR_MEDIA_PREFIX setting. This setting specifies a \
                    URL prefix to the ckeditor JS and CSS media (not \
                    uploaded media). Make sure to use a trailing slash: \
                    CKEDITOR_MEDIA_PREFIX = '/media/ckeditor/'")

        js += (
            settings.STATIC_URL + 'codemirror/js/codemirror.js',
        )
        css = {
            'screen': [
                settings.STATIC_URL + 'codemirror/css/editor.css',
            ]
        }


class ImageInlineAdmin(admin.TabularInline):
    model = SpareImage
    readonly_fields = (
        'code',
    )

    def code(self, obj):
        if obj:
            return u'<textarea style="width:50%"><img src="{0}" width="{1}" height="{2}" alt=""></textarea>'.format(
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
        'comments',
        'filename',
        'path',
    )
    list_display_links = (
        'comments',
        'filename',
    )
    formfield_overrides = {
        TextField: {
            'widget': CodeMirrorOrCKEditorTextArea(),
            # 'widget': Textarea(attrs={'cols': 100, 'rows': 30}),
        },
    }
    inlines = [
        ImageInlineAdmin,
    ]
    fieldsets = (
        (None, {
            'fields': (
                'comments',
                'filename',
                'content',
            )
        }),
        (ugettext_lazy('Render template as site page'), {
            'fields': (
                'path',
                'content_type',
            )
        }),
        (ugettext_lazy('Special'), {
            'fields': (
                'use_wysiwyg',
            )
        }),
    )


admin.site.register(ZeroTemplate, ZeroTemplateAdmin)
