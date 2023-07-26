from flask import Flask, request
import uuid

app = Flask(__name__)


stores = [
    {
        "id": "1",
        "name": "Music Store",
        "items": [{"id": "1", "name": "Piano", "price": 2499.99}],
    }
]


@app.get("/stores")
def get_stores():
    return {"stores": stores}


@app.get("/stores/<string:id>")
def get_store(id):
    for store in stores:
        if store["id"] != id:
            continue
        return store

    return {"message": "Store not found"}, 404


@app.post("/stores")
def create_store():
    request_data = request.get_json()
    new_store = {"id": uuid.uuid1(), "name": request_data["name"], "items": []}
    stores.append(new_store)

    return new_store, 201


@app.get("/stores/<string:id>/items")
def get_items(id):
    for store in stores:
        if store["id"] != id:
            continue
        return store["items"]

    return {"message": "Store not found"}, 404


@app.get("/stores/<string:id>/items/<string:item_id>")
def get_item(id, item_id):
    for store in stores:
        if store["id"] != id:
            continue
        items = store["items"]
        for item in items:
            if item["id"] != item_id:
                continue
            return item

    return {"message": "Store not found"}, 404


@app.post("/stores/<string:id>/items")
def create_item(id):
    request_data = request.get_json()
    for store in stores:
        if store["id"] != id:
            continue
        new_item = {
            "id": uuid.uuid1(),
            "name": request_data["name"],
            "price": request_data["price"],
        }
        store["items"].append(new_item)
        return new_item, 201

    return {"message": "Store not found"}, 401
