import flask
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from flask import current_app

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased
from sqlalchemy.orm.exc import NoResultFound
from project.models import Truck, Trip, Place
from project.database import db
from project.forms import TripForm

session: Session = db.session

truck_blueprint = Blueprint(
    name='truckapp',
    import_name=__name__,
    static_folder='../static',
    url_prefix='/trucks'
)


@truck_blueprint.route('/')
@login_required
def truck_list_view():
    query = select(Truck)
    trucks = session.execute(query).all()
    trucks = [truck[0] for truck in trucks]
    return render_template('truckapp/truck_list.html', trucks=trucks)


@truck_blueprint.route('/<int:id>')
@login_required
def truck_detail_view(id):
    try:
        truck = session.query(Truck).filter(Truck.id == id).one()
    except NoResultFound as exc:
        current_app.logger.error(exc)
        raise
    return render_template('truckapp/truck_detail.html', truck=truck)


@truck_blueprint.route('/trips')
@login_required
def trip_list_view():
    current_page = request.args.get(key='page', default=1, type=int)
    departure = aliased(Place)
    arrival = aliased(Place)
    trip_pagination = (
        session.query(Trip)
               .order_by(Trip.departure_at)
               .join(Trip.truck)
               .join(Trip.products)
               .join(departure, departure.id == Trip.departure_place_id)
               .join(arrival, arrival.id == Trip.arrival_place_id)
               .paginate(page=current_page, per_page=5)
    )
    return render_template('truckapp/trip_list.html', trip_pagination=trip_pagination)


@truck_blueprint.route('/trips/create', methods=["GET", "POST"])
@login_required
def trip_create():
    error = None
    form = TripForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        try:
            form.save()
        except Exception:
            current_app.logger.exception("Could not create trip!")
            error = "Could not create trip!"
        else:
            return redirect(url_for("truckapp.trip_list_view"))
    return flask.render_template("truckapp/trip_create.html", form=form, error=error)
