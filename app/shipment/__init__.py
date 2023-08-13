import hashlib
import time
import datetime
from flask import Blueprint, render_template, request, redirect
import flask_wtf as fw
import wtforms as wt
from wtforms.validators import DataRequired
from app.models import Customer, Shipment


bp = Blueprint('shipment', __name__, url_prefix='/shipment')

class NewShipmentForm(fw.FlaskForm):
    to_name = wt.StringField('To Name', validators=[DataRequired()])
    to_hp = wt.StringField('To HP', validators=[DataRequired()])
    to_addr1 = wt.StringField('To Addr1', validators=[DataRequired()])
    to_addr2 = wt.StringField('To Addr2', validators=[DataRequired()])
    from_name = wt.StringField('From Name', validators=[DataRequired()])
    from_hp = wt.StringField('From HP', validators=[DataRequired()])
    epu = wt.DateField('Pickup', default=datetime.date.today(), description='Pickup Date')
    eta = wt.DateField('ETA', default=datetime.date.today() + datetime.timedelta(days=14))

    submit = wt.SubmitField('Sign In')

def get_awb_num():
    return str(int(hashlib.sha256((str(time.time()) + '!salt!').encode('utf-8')).hexdigest()[:13], 16)).zfill(16)

@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = NewShipmentForm()
    if form.validate_on_submit():
        new_shipment = Shipment(**form.data)
        new_shipment.awb = get_awb_num()
        new_shipment.description = ''
        new_shipment.save()
        return redirect('/')
    custs = Customer.select().order_by(Customer.name)
    return render_template('shipment/add.html', form=form, customer=custs)

@bp.route('/<awb>')
def show(awb):
    return render_template('shipment/show.html', awb=awb)

@bp.route('')
def index():
    shipments = Shipment.select().order_by(Shipment.id.desc())
    return render_template('shipment/index.html', shipments=shipments)

