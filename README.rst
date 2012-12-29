====================
django-live-profiler
====================

Profile Django-based applications running in production with minimal performance overhead.

---------
Rationale
---------
Profiling web applications on a development environment often produces misleading results due to different patterns in the data, different patterns in user behavior and differences in infrastructure. 

All existing DB access profiling solutions for Django seem to be focusing on a single request. However, in the real world certain queries might be negligible in a single request while still puttin a considerable strain the database across all requests.

*django-live-profiler* aims to solve these issues by collecting database usage data from a live application.

.. image :: https://github.com/InviteBox/django-live-profiler/raw/master/doc/screenshot1.png
   :alt: screenshot

------------
Requirements
------------
*django-live-profiler* currently requires MongoDB to store query data. 

------------
Installation
------------
1. Run `pip install django-live-profiler`
2. Add `'profiler'` app to `INSTALLED_APPS` 
3. Add `'profiler.middleware.ProfilerMiddleware'` to `MIDDLEWARE_CLASSES`
4. Add `url(r'^profiler/', include('profiler.urls'))` to your urlconf


Visit http://yoursite.com/profiler/ for results.
