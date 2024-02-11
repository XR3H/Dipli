class Table:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.max_cap = kwargs.get('max_cap')

    def getData(self):
        return [self.id, self.name, self.max_cap]

class User:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.email = kwargs.get('email')

    def getData(self):
        return [self.id, self.username, self.password, self.email]

class ReservationStatus:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')

    def getData(self):
        return [self.id, self.name]

class Reservation:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.table = kwargs.get('table')
        self.client = kwargs.get('client')
        self.res_date = kwargs.get('res_date')
        self.leave_date = kwargs.get('leave_date')
        self.wishes = kwargs.get('wishes')
        self.ref_name = kwargs.get('ref_name')
        self.tel_no = kwargs.get('tel_no')
        self.status = kwargs.get('status')

    def getData(self):
        return [self.id, self.table, self.client, self.res_date, self.leave_date, self.wishes, self.ref_name, self.tel_no, self.status]

class Meal:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.desc = kwargs.get('desc')
        self.cost = kwargs.get('cost')

    def getData(self):
        return [self.id, self.name, self.desc, self.cost]

class OrderStatus:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')

    def getData(self):
        return [self.id, self.name]

class Order:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.res = kwargs.get('res')
        self.status = kwargs.get('status')
        self.pref = kwargs.get('pref')
        self.meals = kwargs.get('meals')

    def getData(self):
        return [self.id, self.res, self.status, self.pref, self.meals]

class MealPresense:

    def __init__(self, meal, amount, cost):
        self.meal = meal
        self.amount = amount
        self.cost = cost

    def getData(self):
        return [self.meal, self.amount, self.cost]

class Category:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')

    def getData(self):
        return [self.id, self.name]
