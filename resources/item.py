from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint(
    "Item",
    __name__,
    description="Operations on items",
    url_prefix="/items",
)


@blp.route("")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        try:
            item = ItemModel(**item_data)

            db.session.add(item)
            db.session.commit()
            return item
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")


@blp.route("/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, store_id, item_id):
        pass

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, store_id, item_id):
        pass

    def delete(self, store_id, item_id):
        pass
