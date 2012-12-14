django-profiler
===============

The goal of this project is to create a database access profiler that can be used to profile Django-based applications in production with minimal performance overhead.

##Installation

1. Add `'profiler'` app to `INSTALLED_APPS` 
2. Add `'profiler.middleware.ProfilerMiddleware'` to `MIDDLEWARE_CLASSES`
3. Add `url(r'^profiler/', include('profiler.urls'))` to your urlpatterns


Visit http://yoursite.com/profiler/ for results.
