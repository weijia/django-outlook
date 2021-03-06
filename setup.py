#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [
    'django-mailbox',
    'python-social-auth',
    'social-auth-app-django',
    'o365<1.0',
]

test_requirements = [ ]

setup(
    author="Richard Wang",
    author_email='richardwangwang@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Operate outlook mail from Django",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    # include_package_data=True,
    keywords='django_outlook',
    name='django-outlook',
    packages=find_packages(include=[
        'django_outlook',
        'django_outlook.management',
        'django_outlook.migrations',
        'django_outlook.o365_utils',
                                    ]),
    # package_dir={'django_outlook': 'django_outlook'},
    # package_data={"django_outlook": ["templates/*"]},
    # data_files=[("templates", ["templates/*"])],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/weijia/django-outlook',
    version='0.1.2',
    zip_safe=False,
)
