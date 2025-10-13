import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {
        "id": 1, "title": "Sochi", "name": "test"
    },
    {
        "id": 2, "title": "Dubai", "name": "test"
    },
]

@app.get("/hotels")
def get_hotels(
        id: int | None = Query(default=None, description="Название отеля"),
        title: str | None = Query(default=None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True)
):
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })

    return {"satus": "OK"}


@app.put("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body()
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name


    return {"satus": "OK"}


@app.patch("/hotels/{hotel_id}")
def update_hotel_part(
        hotel_id: int,
        title: str | None = Body(default=None),
        name: str | None = Body(default=None)
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title if title else hotel["title"]
            hotel["name"] = name if name else hotel["name"]


    return {"satus": "OK"}



@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"satus": "OK"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

