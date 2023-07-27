import uuid
from db import items
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema

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
            store_items = items[store_id]
            return list(store_items.values())
        except:
            abort(404, message="Store not found")

    @blp.arguments(ItemSchema)
    def post(self, item_data, store_id):
        try:
            store_items = items[store_id]
            new_item_id = uuid.uuid4().hex
            new_item = {
                **item_data,
                "id": new_item_id,
            }
            store_items[new_item_id] = new_item

            return new_item, 201
        except KeyError:
            abort(404, message="Store not found")


@blp.route("/<string:item_id>")
class Item(MethodView):
    def get(self, store_id, item_id):
        try:
            item = items[store_id][item_id]
            return item
        except KeyError:
            abort(404, message="Store or Item not found")

    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, store_id, item_id):
        try:
            item = items[store_id][item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Store or Item not found")

    def delete(self, store_id, item_id):
        try:
            del items[store_id][item_id]
            return {"message": "Item delete successfully"}
        except KeyError:
            abort(404, message="Store or Item not found")
