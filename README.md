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

Also, don't forget to create 'Admin' and 'Layer 8' groups.
