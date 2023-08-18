import datetime
import peewee as pw
from bcrypt import checkpw, hashpw, gensalt
from playhouse.flask_utils import FlaskDB
from playhouse.shortcuts import model_to_dict
from flask_login import UserMixin

DATABASE = 'sqlite://myshipping.db'

db_wrapper = FlaskDB()

class BaseModel(db_wrapper.Model):
    pass
        

class User(UserMixin, BaseModel):
    '''User Authentication'''
    username = pw.CharField(unique=True)
    password = pw.TextField()
    role = pw.CharField(max_length=1, default='0')
    is_active = pw.BooleanField(default=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)

    def check_password(self, password):
        return checkpw(password.encode(), self.password.encode())
    
    def set_password(self, password):
        self.password = hashpw(password.encode('utf-8'), gensalt())
    
    
class Customer(BaseModel):
    '''Custimer who ship goods'''
    name = pw.CharField(max_length=35, unique=True)
    phone = pw.CharField(max_length=35, null=True)
    addr1 = pw.TextField(null=True)
    addr2 = pw.TextField(null=True)
    city = pw.CharField(max_length=50, null=True)
    city_code = pw.CharField(max_length=5)
    zip = pw.CharField(max_length=5, null=True)
    pic_name = pw.CharField(max_length=35, null=True)
    pic_hp = pw.CharField(max_length=20, null=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    
    def to_dict(self):
        data = model_to_dict(self)
        data.pop('created')
        data.pop('modified')
        return data
    
    
class Vendor(BaseModel):
    '''Vendor shipping'''
    name = pw.CharField(max_length=35, unique=True)
    address = pw.TextField(null=True)
    pic_name = pw.CharField(max_length=35, null=True)
    pic_hp = pw.CharField(max_length=20, null=True)


class Shipment(BaseModel):
    '''Shipment Order'''
    awb = pw.CharField(max_length=35, unique=True)
    customer = pw.ForeignKeyField(Customer, null=True)
    order_date = pw.DateField(default=datetime.date.today)
    from_name = pw.CharField(max_length=35)
    from_hp = pw.CharField(max_length=20)
    from_addr1 = pw.CharField(max_length=50, null=True)
    from_addr2 = pw.CharField(max_length=50, null=True)
    from_zip = pw.IntegerField(null=True)
    to_name = pw.CharField(max_length=35)
    to_hp = pw.CharField(max_length=20)
    to_addr1 = pw.CharField(max_length=50, null=True)
    to_addr2 = pw.CharField(max_length=50, null=True)
    to_city = pw.CharField(max_length=50)
    to_city_code = pw.CharField(max_length=5)
    to_zip = pw.IntegerField(null=True)
    epu = pw.DateTimeField(null=True) # Estimated PickUp time
    eta = pw.DateTimeField(null=True)
    num_items = pw.IntegerField(default=1)
    description = pw.TextField()
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    
    
class ShipmentVendor(BaseModel):
    '''Vendor who provide this shipping'''
    shipment = pw.ForeignKeyField(Shipment)
    vendor = pw.ForeignKeyField(Vendor)
    
    
class ShipmentTrack(BaseModel):
    '''Tracking such shipment'''
    shipment = pw.ForeignKeyField(Shipment)
    timestamp = pw.DateTimeField(default=datetime.datetime.now)
    vendor = pw.ForeignKeyField(Vendor)
    status = pw.CharField(max_length=10, default='created') # 'pickup_transit_lastmile_delivery_delivered_paid'