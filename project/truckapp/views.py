from flask import Blueprint, render_template
from flask_login import login_required
from flask import current_app
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from project.models import Truck
from project.database import db
from project.serializers import TruckSchema

session: Session = db.session

truck_blueprint = Blueprint(
    name='truckapp',
    import_name=__name__,
    static_folder='../static',
    url_prefix='/trucks'
)

truck_schema = TruckSchema()


@truck_blueprint.route('/', endpoint='truck_list_view')
@login_required
def truck_list_view():
    query = select(Truck)
    trucks = session.execute(query).all()
    trucks = [truck[0] for truck in trucks]
    return render_template('truckapp/truck_list.html', trucks=trucks)


@truck_blueprint.route('/<int:id>', endpoint='truck_detail_view')
@login_required
def truck_detail_view(id):
    try:
        truck = session.query(Truck).filter(Truck.id == id).one()
    except NoResultFound as exc:
        current_app.logger.error(exc)
        raise
    return render_template('truckapp/truck_detail.html', truck=truck)


@truck_blueprint.route('/api', endpoint='truck_list_api')
def truck_list_api():
    all_trucks = session.query(Truck).all()
    return truck_schema.dump(all_trucks, many=True)


@truck_blueprint.route('/api/<int:id>', endpoint='truck_detail_api')
def truck_detail_api(id):
    try:
        truck = session.query(Truck).filter(Truck.id == id).one()
    except NoResultFound as exc:
        current_app.logger.error(exc)
        raise
    return truck_schema.dump(truck)
