import hashlib
import time
from flask import Blueprint, render_template, redirect, jsonify, request
import flask_wtf as fw
import wtforms as wt
from playhouse.flask_utils import get_object_or_404
from app.models import Customer

bp = Blueprint('customer', __name__, url_prefix='/customer')

class CustomerForm(fw.FlaskForm):
    name = wt.StringField('Name')
    phone = wt.StringField('Phone')
    addr1 = wt.StringField('Addr1')
    addr2 = wt.StringField('Addr2')
    city = wt.StringField('City')
    city_code = wt.StringField('City Code')
    pic_name = wt.StringField('PIC Name')
    pic_hp = wt.StringField('PIC HP')

    submit = wt.SubmitField('Sign In')


@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = CustomerForm()
    if form.validate_on_submit():
        new_customer = Customer(**form.data)
        new_customer.save()
        return redirect('/customer')
    return render_template('customer/add.html', form=form)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    customer = get_object_or_404(Customer, Customer.id==id)
    form = CustomerForm()
    if form.validate_on_submit():
        form.populate_obj(customer)
        customer.save()
        return redirect('/customer')
    return render_template('customer/edit.html', form=form, customer=customer)

@bp.route('/<id>')
def show(id):
    customer = get_object_or_404(Customer, Customer.id==id)
    if request.args.get('json'):
        return jsonify(customer.to_dict())
    return render_template('customer/show.html', customer=customer)

@bp.route('')
def index():
    customer = Customer.select().order_by(Customer.name.asc())
    if request.args.get('json'):
        ret = []
        for c in customer:
            ret.append(c.to_dict())
        return jsonify(ret)
    return render_template('customer/index.html', customer=customer)

