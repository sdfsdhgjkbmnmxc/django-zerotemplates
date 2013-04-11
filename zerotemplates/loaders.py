import os

from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.utils.translation import ugettext

from zerotemplates import DEFAULTS
from zerotemplates.models import ZeroTemplate


class DbLoader(BaseLoader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        try:
            zt = ZeroTemplate.objects.get(filename=template_name)
        except ZeroTemplate.DoesNotExist:
            msg = ugettext('Template {} not found').format(template_name)
            raise TemplateDoesNotExist(msg)
        return zt.content, zt.filename

    load_template_source.is_usable = True


def create_defaults(root, start=''):
    for name in os.listdir(os.path.join(root, start)):
        filename = os.path.join(start, name)
        path = os.path.join(root, filename)
        if os.path.isfile(path):
            ZeroTemplate.objects.get_or_create(
                filename=filename,
                defaults=dict(
                    content=open(path).read(),
                ),
            )
        elif os.path.isdir(path):
            create_defaults(root, filename)

if DEFAULTS:
    create_defaults(DEFAULTS)
