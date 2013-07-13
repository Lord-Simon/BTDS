from distutils.core import setup
setup(name='BTDS',
    description='Multi-Lingual Novel Presentation Platform',
    version='0.1',
    author='Simon',
    author_email='admin@m-chan.org',
    url='https://github.com/Lord-Simon/BTDS/',
    packages=['btds'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "Django >= 1.4.0",
        "django-bootstrap-toolkit >= 2.12.1",
    ],
)
