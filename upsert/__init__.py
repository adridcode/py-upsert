# http://micheles.googlecode.com/hg/decorator/documentation.html
from decorator import decorator
def _memoize(func, *args, **kw):
    if kw: # frozenset is used to ensure hashability
        key = args, frozenset(kw.iteritems())
    else:
        key = args
    cache = func.cache # attributed added by memoize
    if key in cache:
        return cache[key]
    else:
        cache[key] = result = func(*args, **kw)
        return result
def memoize(f):
    f.cache = {}
    return decorator(_memoize, f)

from upsert.ansi_ident import AnsiIdent
from upsert.merge_function import MergeFunction
from upsert.row import Row
from upsert.sqlite3 import Sqlite3
from upsert.mysql import Mysql

class Upsert:
    """
    TBD the description oh yah
    """

    def __init__(self, cursor, table_name):
        self.cursor = cursor
        self.table_name = table_name
        self.implementation = Upsert.implementations[str(type(cursor))](self)

    # Thinking in Python: Fronting for an Implementation
    def __getattr__(self, name):
        return getattr(self.implementation, name)

    def row(self, selector, setter = None):
        if setter is None:
            setter = {}
        self.buffer.append(self.row_class(self, selector, setter))
        self.ready()
        return None

    def execute3(self, template, idents, values):
        pass1 = self.fill_ident_placeholders(template, idents)
        self.execute(pass1, values)
    
    def fill_ident_placeholders(self, template, idents):
        quoted = tuple(self.quote_ident(str) for str in idents)
        return template % quoted

    sqlite3_key =     "<type 'sqlite3.Cursor'>"
    mysql_key =       "<class 'MySQLdb.cursors.Cursor'>"
    # postgresql_key =  "<type 'psycopg2._psycopg.connection'>"

    implementations = {
        sqlite3_key:    Sqlite3,
        mysql_key:      Mysql,
        # postgresql_key: Postgresql
    }
