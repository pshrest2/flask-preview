from flask import Flask, request
from db import stores
from flask_smorest import abort

import uuid

app = Flask(__name__)


@app.get("/stores")
def get_stores():
    return list(stores.values())


@app.get("/stores/<string:id>")
def get_store(id):
    try:
        return stores[id]
    except KeyError:
        abort(404, message="Store not found")


@app.put("/stores/<string:id>")
def update_store(id):
    store_data = request.get_json()
    try:
        store = stores[id]
        store |= store_data
        return store
    except KeyError:
        abort(404, message="Store not found")


@app.delete("/stores/<string:id>")
def delete_store(id):
    try:
        del stores[id]
        return {"message": "Store delete successfully"}
    except KeyError:
        abort(404, message="Store not found")


@app.post("/stores")
def create_store():
    store_data = request.get_json()
    id = uuid.uuid4().hex
    new_store = {**store_data, "id": id}
    stores[id] = new_store

    return new_store, 201


@app.get("/stores/<string:id>/items")
def get_items(id):
    try:
        store = stores[id]
        return list(store["items"].values())
    except:
        abort(404, message="Store not found")


@app.get("/stores/<string:id>/items/<string:item_id>")
def get_item(id, item_id):
    try:
        store = stores[id]
        item = store["items"][item_id]
        return item
    except KeyError:
        abort(404, message="Store or Item not found")


@app.put("/stores/<string:id>/items/<string:item_id>")
def update_item(id, item_id):
    item_data = request.get_json()
    try:
        item = stores[id]["items"][item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message="Store or Item not found")


@app.delete("/stores/<string:id>/items/<string:item_id>")
def delete_item(id, item_id):
    try:
        store = stores[id]
        del store["items"][item_id]
        return {"message": "Item delete successfully"}
    except KeyError:
        abort(404, message="Store or Item not found")


@app.post("/stores/<string:id>/items")
def create_item(id):
    item_data = request.get_json()
    try:
        store = stores[id]
        new_item_id = uuid.uuid4().hex
        new_item = {
            **item_data,
            "id": new_item_id,
        }
        store["items"][new_item_id] = new_item

        return new_item, 201
    except KeyError:
        abort(404, message="Store not found")
