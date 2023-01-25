import flask
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from project.models import User, Truck, Place, Product, Trip
from project.database import db


class TruckIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated or not current_user.is_active:
            flask.flash('Для доступа необходимо войти', 'alert-danger')
            return redirect(url_for("authapp.login_view"))
        return super().index()


admin = Admin(
    name="Truck Admin",
    index_view=TruckIndexView(),
    template_mode="bootstrap4",
)


class BaseModelView(ModelView):
    create_modal = True
    edit_modal = True

    def is_accessible(self):
        is_admin_login = current_user.is_authenticated and current_user.is_superuser
        is_staff_login = current_user.is_authenticated and current_user.is_staff
        return is_admin_login or is_staff_login

    def inaccessible_callback(self, name, **kwargs):
        flask.flash('Недостаточно прав для просмотра', 'alert-danger')
        return redirect(url_for("authapp.login_view"))


class UserAdminView(BaseModelView):
    column_searchable_list = [
        'username',
        'firstname',
        'lastname'
    ]
    column_exclude_list = ['password']
    column_select_related_list = [
        'trucks',
    ]

    def is_accessible(self):
        is_admin_login = current_user.is_authenticated and current_user.is_superuser
        return is_admin_login


class TruckAdminView(BaseModelView):
    column_searchable_list = ['name']
    column_list = [
        'id',
        'name',
        'driver.username',
        'dt_created'
    ]
    column_select_related_list = ['driver']


class ProductAdminView(BaseModelView):
    column_searchable_list = ['name']
    column_list = [
        'id',
        'name',
    ]


class PlaceAdminView(BaseModelView):
    column_searchable_list = ['name']
    column_list = [
        'id',
        'name',
    ]


class TripAdminView(BaseModelView):
    column_searchable_list = ['truck.name']
    column_list = [
        'id',
        'truck.name',
        'departure_place.name',
        'departure_at',
        'arrival_place.name',
        'arrival_at',
        'products'
    ]
    column_select_related_list = [
        'truck',
        'departure_place',
        'arrival_place',
        'products'
    ]


admin.add_view(UserAdminView(User, db.session, category='Users'))
admin.add_view(TruckAdminView(Truck, db.session, category='Trip'))
admin.add_view(ProductAdminView(Product, db.session, category='Trip'))
admin.add_view(PlaceAdminView(Place, db.session, category='Trip'))
admin.add_view(TripAdminView(Trip, db.session, category='Trip'))
