from distutils.core import setup


setup(
    name='django-zerotemplates',
    version='1.0',
    description='',
    author='Maxim Oransky',
    author_email='maxim.oransky@gmail.com',
    license='WTFPL',
    url='http://github.com/sdfsdhgjkbmnmxc/django-zerotemplates',
    packages=[
        'zerotemplates',
    ],
    install_requires=open('requirements.txt').readlines(),
    package_data={
        'zerotemplates': [
            'locale/ru/LC_MESSAGES/*',
            'static/codemirror/css/*',
            'static/codemirror/js/*',
        ],
    },
)
