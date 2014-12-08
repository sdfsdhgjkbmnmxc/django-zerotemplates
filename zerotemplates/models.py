from django.core.exceptions import ValidationError
from django.template import loader, Context, TemplateSyntaxError
from django.utils.translation import ugettext_lazy, ugettext
from django.db import models


content_type_choices = (
    'text/html',
    'text/plain',
    'text/xml',
    'text/css',
)


class ZeroTemplate(models.Model):
    filename = models.CharField(
        ugettext_lazy('template name'),
        unique=True,
        db_index=True,
        help_text=ugettext_lazy('Example: my_page.html'),
        max_length=120,
    )
    path = models.CharField(
        ugettext_lazy('path'),
        blank=True,
        default='',
        help_text=ugettext_lazy('Example: /my-page/. Optional'),
        max_length=200,
    )
    content = models.TextField(
        ugettext_lazy('content'),
        blank=True,
        default='',
    )
    comments = models.CharField(
        ugettext_lazy('comments'),
        blank=True,
        default='',
        help_text=ugettext_lazy('internal use only'),
        max_length=4800,
    )
    content_type = models.CharField(
        'Content-type',
        default=content_type_choices[0],
        max_length=50,
        choices=[(x, x) for x in content_type_choices],
    )
    use_wysiwyg = models.BooleanField(
        ugettext_lazy('Use WYSIWG editor'),
        help_text=ugettext_lazy('Press "Save" for apply'),
        default=False,
    )

    def clean(self):
        self.filename = (self.filename or '').strip().lower()
        self.path = (self.path or '').strip().lower()

        try:
            content = loader.get_template_from_string(self.content).render(Context())
        except TemplateSyntaxError as e:
            raise ValidationError({
                'content': unicode(e),
            })

        if self.use_wysiwyg and content.strip() != self.content.strip():
            self.use_wysiwyg = False
            raise ValidationError({
                'use_wysiwyg': ugettext('Can\'t use WYSIWG editor for django templates'),
            })

    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super(ZeroTemplate, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.filename

    class Meta:
        verbose_name = ugettext_lazy('template')
        verbose_name_plural = ugettext_lazy('templates')
        ordering = ('filename',)


class SpareImage(models.Model):
    zero_template = models.ForeignKey(ZeroTemplate)
    image = models.ImageField(upload_to='spares')

    def __unicode__(self):
        return u'#{}'.format(self.id)

    class Meta:
        verbose_name = ugettext_lazy('image')
        verbose_name_plural = ugettext_lazy('images')
        ordering = ('-id',)
