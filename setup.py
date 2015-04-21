from setuptools import setup, find_packages

setup(
    name = "django-social-timeline",
    version = "0.1",
    author = "David Burke",
    author_email = "david@thelabnyc.com",
    description = ("Social networking for django. Following system and timeline of events."),
    license = "Apache License",
    keywords = ["django", "social networking"],
    url = "https://github.com/thelabnyc/django-social-timeline",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=[
    ]
)
