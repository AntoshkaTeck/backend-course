async def test_add_booking(auth_ac, db):
    room_id = (await db.rooms.get_all())[0].id
    response = await auth_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": "2025-11-01",
            "date_to": "2025-11-30",

        }
    )
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "OK"
    assert isinstance(res, dict)
    assert "data" in res
