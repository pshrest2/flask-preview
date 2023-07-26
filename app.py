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
def get_store():
    return {"stores": stores}


@app.post("/stores")
def create_store():
    request_data = request.get_json()
    new_store = {"id": uuid.uuid1(), "name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/stores/<string:id>/items")
def create_item(id):
    request_data = request.get_json()
    for store in stores:
        if store["id"] == id:
            new_item = {
                "id": uuid.uuid1(),
                "name": request_data["name"],
                "price": request_data["price"],
            }
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 401
