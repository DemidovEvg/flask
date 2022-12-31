from flask import Blueprint, render_template, g
from flask_login import login_required
from sqlalchemy import select
from project.models import Truck


truck_blueprint = Blueprint(
    name='truckapp',
    import_name=__name__,
    static_folder='../static',
    url_prefix='/trucks'
)


@truck_blueprint.route('/', endpoint='truck_list_view')
@login_required
def truck_list_view():
    query = select(Truck)
    trucks = g.session.execute(query).all()
    trucks = [truck[0] for truck in trucks]
    return render_template('truckapp/truck_list.html', trucks=trucks)


@truck_blueprint.route('/<int:id>', endpoint='truck_detail_view')
@login_required
def truck_detail_view(id):
    truck = g.session.query(Truck).filter(Truck.id == id).one()
    return render_template('truckapp/truck_detail.html', truck=truck)
