"""Simple CLI utilities for offline maintenance tasks."""
import argparse
import csv
from audit_tool import create_app, db
from audit_tool.models import Audit


def export_csv(path: str) -> None:
    app = create_app()
    with app.app_context():
        rows = Audit.query.all()
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'severity', 'status'])
            for a in rows:
                writer.writerow([a.id, a.title, a.severity, a.status])
    print(f'Exported {len(rows)} audits to {path}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Audit tool maintenance CLI')
    parser.add_argument('--export', metavar='PATH', help='Export audits to CSV')
    args = parser.parse_args()
    if args.export:
        export_csv(args.export)


if __name__ == '__main__':
    main()
