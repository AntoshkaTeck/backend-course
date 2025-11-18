"""cascade delete booking

Revision ID: 60c6c5d21aed
Revises: 36f9a9cffcee
Create Date: 2025-11-17 00:29:19.957827

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "60c6c5d21aed"
down_revision: Union[str, Sequence[str], None] = "36f9a9cffcee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f("bookings_room_id_fkey"), "bookings", type_="foreignkey")
    op.create_foreign_key(None, "bookings", "rooms", ["room_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.create_foreign_key(op.f("bookings_room_id_fkey"), "bookings", "rooms", ["room_id"], ["id"])
