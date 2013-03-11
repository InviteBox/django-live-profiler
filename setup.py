import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if os.path.exists('README.rst'):
    long_description = read('README.rst')
else:
    long_description = 'https://github.com/InviteBox/django-live-profiler'

setup(
    name = "django-live-profiler",
    version = "0.0.9",
    author = "Alexander Tereshkin",
    author_email = "atereshkin@invitebox.com",
    description = ("A database access profiler for Django-based applications that can be ran in production "
                                   "with minimal performace overhead."),
    license = "BSD",
    keywords = "django profiler",
    url = "https://github.com/InviteBox/django-live-profiler",
    packages=['profiler','aggregate'],
    long_description=long_description,
    install_requires=('pyzmq', 'statprof'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",        
    ],
    include_package_data=True,
        entry_points={
        'console_scripts': ['aggregated = aggregate.server:main'],
    },

)
