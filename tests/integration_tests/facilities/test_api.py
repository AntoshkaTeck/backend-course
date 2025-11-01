async def test_get_facilities(ac):
    response = await ac.get("/facilities/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_facility(ac):
    facility_title = "Парковка"
    response = await ac.post(
        "/facilities/",
        json={
            "title": facility_title
        }
    )
    assert response.status_code == 200
    res = response.json().get("data")
    assert isinstance(res, dict)
    assert res
    assert res["title"] == facility_title


