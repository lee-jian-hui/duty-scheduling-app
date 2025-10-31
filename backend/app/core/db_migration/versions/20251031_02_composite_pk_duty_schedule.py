"""Switch duty_schedule to composite PK (date, staff_id)

Revision ID: 02_composite_pk
Revises: c9d0ad70cfbf
Create Date: 2025-10-31 20:15:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '02_composite_pk'
down_revision = 'c9d0ad70cfbf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # SQLite: rebuild table to change primary key
    op.create_table(
        'duty_schedule_new',
        sa.Column('date', sa.String(length=10), nullable=False),
        sa.Column('staff_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('date', 'staff_id'),
    )

    # Copy data from old table; old schema had unique date, choose existing rows
    conn = op.get_bind()
    conn.execute(sa.text(
        'INSERT INTO duty_schedule_new(date, staff_id) SELECT date, staff_id FROM duty_schedule'
    ))

    op.drop_table('duty_schedule')
    op.rename_table('duty_schedule_new', 'duty_schedule')


def downgrade() -> None:
    # Downgrade to PK on date only; potential data loss if multiple rows per date exist.
    op.create_table(
        'duty_schedule_old',
        sa.Column('date', sa.String(length=10), nullable=False),
        sa.Column('staff_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('date'),
    )

    conn = op.get_bind()
    # Keep one row per date (choose smallest staff_id)
    conn.execute(sa.text(
        'INSERT INTO duty_schedule_old(date, staff_id) '
        'SELECT date, MIN(staff_id) FROM duty_schedule GROUP BY date'
    ))

    op.drop_table('duty_schedule')
    op.rename_table('duty_schedule_old', 'duty_schedule')

