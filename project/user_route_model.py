

from os import access
from threading import activeCount
from marshmallow import Schema,fields
from pkg_resources import require

#Parameter(Schema)
class UserPostRequests(Schema):
    name=fields.Str(doc="name",required=True)
    price=fields.Str(doc="price",required=True)
    quantity=fields.Str(doc="quantity",required=True)

class UserPatchRequest(Schema):
    name = fields.Str(doc="name")
    price = fields.Str(doc="price")
    quantity=fields.Str(doc="quantity")


#Response




# Common
class UserCommonResponse(Schema):
    message = fields.Str(example="success")




class UserGetResponse(UserCommonResponse):
    data=fields.List(fields.Dict(),example={
        "name":"apple",
        "price":"100",
        "quantity":"1",
        
    })
    datatime=fields.Str()



class LoginRequests(Schema):
    account=fields.Str(doc='account',required=True)
    password=fields.Str(do="passwd",required=True)

class RegisterRequests(Schema):
    id = fields.Str(doc="id")
    name = fields.Str(doc="name")
    birth = fields.Str(doc="birth")
    gender = fields.Str(doc="gender")
    account=fields.Str(doc='account',required=True)
    password=fields.Str(do="passwd",required=True)

class SearchProduct(Schema):
    name = fields.Str(doc="word",required=True)

