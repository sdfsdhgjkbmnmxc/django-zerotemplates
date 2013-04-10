import os

from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.utils.translation import ugettext

from zerotemplates import DEFAULTS
from zerotemplates.models import ZeroTemplate


class DbLoader(BaseLoader):
    is_usable = True

    def create_defaults(self):
        if not DEFAULTS:
            return
        for filename in os.listdir(DEFAULTS):
            if os.path.isfile(filename):
                ZeroTemplate.objects.get_or_create(
                    filename=filename,
                    defaults=dict(
                        content=open(filename).read(),
                    ),
                )

    def load_template_source(self, template_name, template_dirs=None):
        try:
            zt = ZeroTemplate.objects.get(filename=template_name)
        except ZeroTemplate.DoesNotExist:
            self.create_defaults()
            try:
                zt = ZeroTemplate.objects.get(filename=template_name)
            except ZeroTemplate.DoesNotExist:
                msg = ugettext('Template {} not found').format(template_name)
                raise TemplateDoesNotExist(msg)
        return zt.content, zt.filename

    load_template_source.is_usable = True
