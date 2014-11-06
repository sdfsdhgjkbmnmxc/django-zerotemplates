django-zerotemplates
====================

Simple analog of django-dbtemplates.

Install:
```
pip install git+https://github.com/sdfsdhgjkbmnmxc/django-zerotemplates.git#egg=zerotemplates
```

settings.py:
```python
    INSTALLED_APPS = (
        # ....
        'zerotemplates',
    )
    TEMPLATE_LOADERS = (
        # ...
        'zerotemplates.loaders.DbLoader',
    )
```
