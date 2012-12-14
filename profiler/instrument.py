from datetime import datetime

from django.db.models.sql.compiler import SQLCompiler
from django.db import connection

from profiler.backends import get_backend

def execute_sql(self, *args, **kwargs):
    backend = get_backend()
    if backend is None:
        return self.__execute_sql(*args, **kwargs)
    q, params = self.as_sql()
    start = datetime.now()
    try:
        return self.__execute_sql(*args, **kwargs)
    finally:
        d = (datetime.now() - start)
        backend.log_query(q, d.seconds * 1000 + d.microseconds/1000)
        
INSTRUMENTED = False



if not INSTRUMENTED:
    SQLCompiler.__execute_sql = SQLCompiler.execute_sql
    SQLCompiler.execute_sql = execute_sql
    INSTRUMENTED = True

