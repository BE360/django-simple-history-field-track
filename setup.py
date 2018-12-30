from setuptools import setup, find_packages

setup(
    name='django-simple-history-field-track',
    version='0.0.3',
    description='Additional field tracker to django-simple-history with admin integration',
    packages=find_packages(),
    long_description='\n'.join((
        open('README.rst').read(),
    )),
    author='Armin Mohammadi',
    author_email='armin.mohamady@gmail.com',
    maintainer='Armin Mohammadi',
    url='',
    install_requires=[
        'django-simple-history==2.5.1'
    ],
    classifiers=[
        "Development Status :: Development",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: BSD License",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    include_package_data=True,
)