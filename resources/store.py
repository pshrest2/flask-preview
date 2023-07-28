from sqlalchemy.exc import SQLAlchemyError

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from db import db
from models import StoreModel

blp = Blueprint(
    "Store", __name__, description="Operations on stores", url_prefix="/stores"
)


@blp.route("")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        try:
            store = StoreModel(**store_data)

            db.session.add(store)
            db.session.commit()
            return store
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store.")


@blp.route("/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        pass

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        pass

    def delete(self, store_id):
        pass
