from flask import Blueprint, render_template, g
from sqlalchemy import select
from models import Truck


truck_blueprint = Blueprint(
    name='truck',
    import_name=__name__,
    static_folder='../static',
    url_prefix='/trucks'
)


@truck_blueprint.route('/', endpoint='truck_list_view')
def truck_list_view():
    query = select(Truck)
    trucks = g.session.execute(query).all()
    trucks = [truck[0] for truck in trucks]
    return render_template('truck/truck_list.html', trucks=trucks)


@truck_blueprint.route('/<int:id>', endpoint='truck_detail_view')
def truck_detail_view(id):
    truck = g.session.query(Truck).filter(Truck.id == id).one()
    return render_template('truck/truck_detail.html', truck=truck)
