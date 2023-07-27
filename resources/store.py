import uuid
from db import stores
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

blp = Blueprint(
    "Store", __name__, description="Operations on stores", url_prefix="/stores"
)


@blp.route("")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store

        return new_store


@blp.route("/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
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
