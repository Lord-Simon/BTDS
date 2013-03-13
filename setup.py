from distutils.core import setup
setup(name='BTDS',
    description='Multi-Lingual Novel Presentation Platform',
    author='Simon',
    author_email='',
    url='https://github.com/Lord-Simon/BTDS/',
    packages=['btds'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "Django >= 1.4.0",
    ],
)
