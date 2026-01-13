"""Verify database schema after migration."""
from app.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)

print("=== Users Table Schema ===")
print("\nColumns:")
for col in inspector.get_columns('users'):
    print(f"  - {col['name']}: {col['type']} (nullable={col['nullable']})")

print("\nIndexes:")
for idx in inspector.get_indexes('users'):
    print(f"  - {idx['name']}: columns={idx['column_names']}, unique={idx['unique']}")

print("\n=== Tasks Table Schema ===")
print("\nColumns:")
for col in inspector.get_columns('tasks'):
    print(f"  - {col['name']}: {col['type']} (nullable={col['nullable']})")

print("\nForeign Keys:")
for fk in inspector.get_foreign_keys('tasks'):
    print(f"  - {fk['name']}: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")

print("\nIndexes:")
for idx in inspector.get_indexes('tasks'):
    print(f"  - {idx['name']}: columns={idx['column_names']}, unique={idx['unique']}")

print("\n✓ Database schema verification complete")
