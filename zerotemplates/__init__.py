from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


DEFAULTS = getattr(settings, 'ZEROTEMPLATES_DEFAULTS', '')

_loader_name = 'zerotemplates.loaders.DbLoader'
if not _loader_name in settings.TEMPLATE_LOADERS:
    raise ImproperlyConfigured('Add {} to settings.TEMPLATE_LOADERS'.format(
        _loader_name,
    ))
