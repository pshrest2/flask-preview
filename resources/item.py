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
    def get(self, item_id):
        return ItemModel.query.get_or_404(item_id)

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        item.price = item_data["price"]
        item.name = item_data["name"]

        db.session.add(item)
        db.session.commit()

        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}
