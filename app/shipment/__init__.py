import hashlib
import time
from flask import Blueprint, render_template, request
import flask_wtf as fw
import wtforms as wt


bp = Blueprint('shipment', __name__, url_prefix='/shipment')

class NewShipmentForm(fw.FlaskForm):
    to_name = wt.StringField('To Name')
    to_hp = wt.StringField('To HP')
    to_addr1 = wt.StringField('To Addr1')
    to_addr2 = wt.StringField('To Addr2')

    submit = wt.SubmitField('Sign In')

def get_awb_num():
    return str(int(hashlib.sha256((str(time.time()) + '!salt!').encode('utf-8')).hexdigest()[:13], 16)).zfill(16)

@bp.route('/add')
def add():
    form = NewShipmentForm()
    return render_template('shipment/add.html', form=form)

@bp.route('/<awb>')
def show(awb):
    return render_template('shipment/show.html', awb=awb)

@bp.route('')
def index():
    return render_template('shipment/index.html')

