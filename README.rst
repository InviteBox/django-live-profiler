====================
django-live-profiler
====================

Django-live-profiler is a low-overhead data access and code profiler for Django-based applications. For more information, check out http://invitebox.github.com/django-live-profiler/

------------
Installation
------------
1. Run `pip install django-live-profiler`
2. Add `'profiler'` app to `INSTALLED_APPS` 
3. Add `'profiler.middleware.ProfilerMiddleware'` to `MIDDLEWARE_CLASSES`
4. Optionally add `'profiler.middleware.StatProfMiddleware'` to `MIDDLEWARE_CLASSES` to enable Python code statistical profiling (using statprof_). WARNING: this is an experimental feature, beware of possible incorrect output.
5. Add `url(r'^profiler/', include('profiler.urls'))` to your urlconf

.. _statprof: https://github.com/bos/statprof.py

-----
Usage
-----

In order to start gathering data you need to start the aggregation server::

  $ aggregated --host 127.0.0.1 --port 5556


Visit http://yoursite.com/profiler/ for results.
