from django.conf.urls import patterns, url
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from zerotemplates.models import ZeroTemplate


def display_page(request):
    zp = get_object_or_404(ZeroTemplate, path=request.path)
    return TemplateResponse(request, zp.filename, content_type=zp.content_type)


urlpatterns = patterns(
    '',
    url('^', display_page),
)
