import pytest

from tests.conftest import get_db_null_pull


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-11-01", "2025-11-30", 200),
        (1, "2025-11-01", "2025-11-30", 200),
        (1, "2025-11-01", "2025-11-30", 200),
        (1, "2025-11-01", "2025-11-30", 200),
        (1, "2025-11-01", "2025-11-30", 200),
        (1, "2025-11-01", "2025-11-30", 409),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, auth_ac, db):
    response = await auth_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert res["status"] == "OK"
        assert isinstance(res, dict)
        assert "data" in res


@pytest.fixture(scope="module")
async def del_all_bookings():
    async for db_ in get_db_null_pull():
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booking_count",
    [
        (1, "2025-11-01", "2025-11-05", 1),
        (1, "2025-11-10", "2025-11-20", 2),
        (1, "2025-12-01", "2025-12-10", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id, date_from, date_to, booking_count, auth_ac, del_all_bookings
):
    await auth_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    response = await auth_ac.get("/bookings/me")
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == booking_count
