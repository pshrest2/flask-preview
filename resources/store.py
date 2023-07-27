import uuid
from db import stores
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint(
    "Store", __name__, description="Operations on stores", url_prefix="/stores"
)


@blp.route("")
class StoreList(MethodView):
    def get(self):
        return list(stores.values())

    def post(self):
        store_data = request.get_json()
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store

        return new_store, 201


@blp.route("/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    def put(self, store_id):
        store_data = request.get_json()
        try:
            store = stores[store_id]
            store |= store_data
            return store
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store delete successfully"}
        except KeyError:
            abort(404, message="Store not found")
