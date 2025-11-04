import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2025-11-01", "2025-11-30", 200),
    (1, "2025-11-01", "2025-11-30", 200),
    (1, "2025-11-01", "2025-11-30", 200),
    (1, "2025-11-01", "2025-11-30", 200),
    (1, "2025-11-01", "2025-11-30", 200),
    (1, "2025-11-01", "2025-11-30", 403),
])
async def test_add_booking(room_id,
                           date_from,
                           date_to,
                           status_code,
                           auth_ac, db):
    response = await auth_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,

        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert res["status"] == "OK"
        assert isinstance(res, dict)
        assert "data" in res
