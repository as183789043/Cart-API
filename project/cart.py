from pydoc import describe
from flask_restful import Resource, reqparse
import pymysql
from flask import jsonify
import util
from flask_apispec import doc,use_kwargs,MethodResource,marshal_with
from user_route_model import UserGetResponse,UserCommonResponse,UserPatchRequest,UserPostRequests,LoginRequests,RegisterRequests,SearchProduct
from flask_jwt_extended import create_access_token,jwt_required
from datetime import timedelta 

def db_init():
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        db='shopping_cart'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

def get_access_token(account):
    token = create_access_token(
        identity={"account": account},
        expires_delta=timedelta(days=1)
    )
    return token

class Carts(MethodResource):
    @doc(description='Get cart info',tags=['Carts'])
    @marshal_with(UserGetResponse,code=200)
    @jwt_required()
    def get(self):
        db, cursor = db_init()

        sql = "SELECT * FROM shopping_cart.fruit "
        cursor.execute(sql)
        

        users = cursor.fetchall()
        db.close()
        return util.success(users)

    @doc(description='Post cart info',tags=['Carts'])
    @use_kwargs(UserPostRequests,location="json")
    @marshal_with(UserCommonResponse,code=200)
    def post(self,**kwargs):
        db, cursor = db_init()
        

        user = {
            'name': kwargs['name'],
            'price': kwargs['price'],
            'quantity': kwargs['quantity'],
        }
        sql = """

        INSERT INTO `shopping_cart`.`fruit` (`name`,`price`,`quantity`)
        VALUES ('{}','{}','{}');

        """.format(
            user['name'], user['price'] ,user['quantity'])
            
        result = cursor.execute(sql)
        
        db.commit()
        db.close()

        if result==1:
            return util.success()
        
        return util.failure()
        
        


class Cart(MethodResource):
    @doc(description='Update cart info',tags=['Carts'])
    @use_kwargs(UserPatchRequest,location="json")
    @marshal_with(UserGetResponse,code=200)
    def patch(self, name,**kwargs):
        db, cursor = db_init()
        
        user = {
            'name': kwargs.get('name'),
            'price': kwargs.get('price'),
            'quantity': kwargs.get('quantity')
            
        }

        query = []
        print(user)
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = {value}")
        query = ",".join(query)
        print(query)
        '''
        UPDATE table_name
        SET column1=value1, column2=value2, column3=value3···
        WHERE some_column=some_value;

        '''
        sql = """
            UPDATE shopping_cart.fruit
            SET {}
            WHERE name = "{}";
        """.format(query, name)
        sql_total="SELECT SUM(CONVERT(price,SIGNED)* CONVERT(quantity,SIGNED)) AS total_price FROM fruit;"

        result = cursor.execute(sql)
        result2 = cursor.execute(sql_total)


        db.commit()
        users = cursor.fetchall()
        db.close()

        if result  ==1:
            return util.success(users)
        
        return util.failure()
        

    @doc(description='Delete cart info',tags=['Carts'])
    @marshal_with(UserGetResponse,code=200)
    def delete(self, name):
        db, cursor = db_init()
        sql = f'DELETE FROM `shopping_cart`.`fruit` WHERE name = "{name}";'
        sql_total="SELECT SUM(CONVERT(price,SIGNED)* CONVERT(quantity,SIGNED)) AS total_price FROM fruit;"
        result = cursor.execute(sql)
        result2 = cursor.execute(sql_total)

        db.commit()
        users = cursor.fetchall()
        db.close()

        if result==1:
            return util.success(users)
        
        return util.failure()

class Login(MethodResource):
    @doc(description='User Login', tags=['Login'])
    @use_kwargs(LoginRequests, location="json") #要改
    #@marshal_with(user_router_model.UserGetResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        account, password = kwargs["account"], kwargs["password"]
        sql = f"SELECT * FROM shopping_cart.member WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()

        if user != ():
            token = get_access_token(account)
            data = {
                "message": f"Welcome back {user[0]['name']}",
                "token": token}
            return util.success(data)
        
        return util.failure({"message":"Account or password is wrong"})


class Register(MethodResource):
    @doc(description='Register member',tags=['Register'])
    @use_kwargs(RegisterRequests,location="json")
    @marshal_with(UserCommonResponse,code=200)
    def post(self,**kwargs):
        db, cursor = db_init()
        

        user = {
            'id': kwargs['id'],
            'name': kwargs['name'],
            'birth': kwargs['birth'],
            'gender':kwargs['gender'],
            'account':kwargs['account'],
            'password':kwargs['password'],
        }
        sql = """

        INSERT INTO `shopping_cart`.`member` (`id`,`name`,`birth`,`gender`,`account`,`password`)
        VALUES ({},'{}','{}','{}','{}','{}');

        """.format(
            user['id'], user['name'] ,user['birth'],user['gender'], user['account'] ,user['password'])
            
        result = cursor.execute(sql)
        
        db.commit()
        db.close()

        if result==1:
            return util.success()
        
        return util.failure()


class search(MethodResource):
    @doc(description='Search cart info',tags=['Search'])
    @marshal_with(UserGetResponse,code=200)
    @jwt_required()
    def get(self, name):
        db, cursor = db_init()
        sql = f'select * FROM `shopping_cart`.`fruit` WHERE name like "%{name}%";'
        result = cursor.execute(sql)

        db.commit()

        users = cursor.fetchall()
        db.close()
        return util.success(users)