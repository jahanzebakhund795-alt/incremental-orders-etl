"""Incremental Orders ETL. Synthetic portfolio demonstration."""
import sqlite3

def run(data):
    with sqlite3.connect(':memory:') as db:
        db.execute('CREATE TABLE orders(id TEXT PRIMARY KEY, amount_cents INTEGER CHECK(amount_cents>=0), version INTEGER)')
        for batch in data['batches']:
            with db:
                for row in batch:
                    if not row['id'] or row['version'] < 1:
                        raise ValueError('Invalid order key or version')
                    db.execute("""INSERT INTO orders VALUES(?,?,?) ON CONFLICT(id)
                        DO UPDATE SET amount_cents=excluded.amount_cents, version=excluded.version
                        WHERE excluded.version > orders.version""",
                        (row['id'], row['amount_cents'], row['version']))
        rows = db.execute('SELECT id,amount_cents,version FROM orders ORDER BY id').fetchall()
        return {'orders': [list(r) for r in rows], 'revenue_cents': sum(r[1] for r in rows)}



if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('sample.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.input.read_text()))
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.write_text(serialized + '\n')
    else:
        print(serialized)
