from django.core.exceptions import ValidationError
from django.template import loader, Context
from django.utils.translation import ugettext_lazy
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
        null=True,
        help_text=ugettext_lazy('Example: /my-page/. Optional'),
        max_length=200,
    )
    content = models.TextField(
        ugettext_lazy('content'),
        blank=True,
        null=True,
    )
    comments = models.CharField(
        ugettext_lazy('comments'),
        blank=True,
        null=True,
        help_text=ugettext_lazy('internal use only'),
        max_length=4800,
    )
    content_type = models.CharField(
        'Content-type',
        default=content_type_choices[0],
        max_length=50,
        choices=[(x, x) for x in content_type_choices],
    )

    def clean(self):
        self.filename = (self.filename or '').strip().lower()
        self.path = (self.path or '').strip().lower()
        try:
            loader.get_template_from_string(self.content).render(Context())
        except Exception as e:
            raise ValidationError({
                'content': unicode(e),
            })

    def save(self, *args, **kwargs):
        self.clean()
        super(ZeroTemplate, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.filename

    class Meta:
        verbose_name = ugettext_lazy('template')
        verbose_name_plural = ugettext_lazy('templates')
        ordering = ('filename',)
