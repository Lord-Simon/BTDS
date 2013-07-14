BTDS
====

Baka-Tsuki Distribution System

Usage
-----
In your `settings.py`:

    INSTALLED_APPS = (
        ...
        'btds'
        ...
    )
    
    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        "btds.context_processors.AddForms",
        "btds.context_processors.BTDSAC",
        ...
    )

Set 'BTDS_GROUP_ADMIN' to your admin group name and 'BTDS_GROUP_USER' to the normal users.
