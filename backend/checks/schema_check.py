"""Compare every application column and foreign key with database/schema.sql.

The reference schema is created inside a transaction and rolled back. No existing
application data is changed. Run from the project root with the backend Python.
"""

from pathlib import Path
import re
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from database import get_db
from psycopg2 import sql


def columns(db, schema):
    """Read the complete column contract without querying account data."""
    rows = db.fetch_all("""
        select table_name, column_name, udt_name, character_maximum_length,
               numeric_precision, numeric_scale, is_nullable, is_identity
        from information_schema.columns where table_schema=%s
        order by table_name, ordinal_position
    """, (schema,))
    return {(r['table_name'], r['column_name']): dict(r) for r in rows}


def foreign_keys(db, schema):
    """Compare relationship definitions independently of constraint names."""
    rows = db.fetch_all("""
        select t.relname as table_name, pg_get_constraintdef(c.oid) as definition
        from pg_constraint c join pg_class t on t.oid=c.conrelid
        join pg_namespace n on n.oid=t.relnamespace
        where n.nspname=%s and c.contype='f'
    """, (schema,))
    return {(r['table_name'], r['definition'].replace(schema + '.', '').replace('public.', '')) for r in rows}


def run():
    """Validate the configured database against a temporary reference schema."""
    db = get_db()
    reference = 'crs_schema_check_' + uuid4().hex
    try:
        current = db.fetch_one('select current_schema() as name')['name']
        actual = columns(db, current)
        actual_fks = foreign_keys(db, current)
        db.execute(sql.SQL('CREATE SCHEMA {}; SET LOCAL search_path TO {}').format(
            sql.Identifier(reference), sql.Identifier(reference)))
        source = (Path(__file__).resolve().parents[2] / 'database/schema.sql').read_text()
        source = re.sub(r'^\s*(begin|commit);\s*$', '', source, flags=re.I | re.M)
        db.execute(source)
        expected = columns(db, reference)
        expected_fks = foreign_keys(db, reference)
        differences = []
        for key in sorted(actual.keys() | expected.keys()):
            if actual.get(key) != expected.get(key):
                differences.append(f'{key}: actual={actual.get(key)}, expected={expected.get(key)}')
        for item in sorted(actual_fks ^ expected_fks):
            differences.append(f'Foreign key differs: {item}')
        if differences:
            raise AssertionError('\n'.join(differences))
        print(f'SCHEMA PASS: {len({k[0] for k in actual})} tables, '
              f'{len(actual)} columns, {len(actual_fks)} foreign keys match schema.sql')
    finally:
        db.conn.rollback()
        db.close()


if __name__ == '__main__':
    run()
