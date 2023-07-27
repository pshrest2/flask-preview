import uuid
from db import stores
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint(
    "Item",
    __name__,
    description="Operations on items",
    url_prefix="/<string:store_id>/items",
)


@blp.route("")
class ItemList(MethodView):
    def get(self, store_id):
        try:
            store = stores[store_id]
            return list(store["items"].values())
        except:
            abort(404, message="Store not found")

    def post(self, store_id):
        item_data = request.get_json()
        try:
            store = stores[store_id]
            new_item_id = uuid.uuid4().hex
            new_item = {
                **item_data,
                "id": new_item_id,
            }
            store["items"][new_item_id] = new_item

            return new_item, 201
        except KeyError:
            abort(404, message="Store not found")


@blp.route("/<string:item_id>")
class Item(MethodView):
    def get(self, store_id, item_id):
        try:
            store = stores[store_id]
            item = store["items"][item_id]
            return item
        except KeyError:
            abort(404, message="Store or Item not found")

    def put(self, store_id, item_id):
        item_data = request.get_json()
        try:
            item = stores[store_id]["items"][item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Store or Item not found")

    def delete(self, store_id, item_id):
        try:
            store = stores[store_id]
            del store["items"][item_id]
            return {"message": "Item delete successfully"}
        except KeyError:
            abort(404, message="Store or Item not found")
