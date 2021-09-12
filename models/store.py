from db import db

class StoreModel(db.Model):
    __tablename__="stores"

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80))

    items=db.relationship("ItemModel",lazy='dynamic')
    # lazy="dynamic" ==> it makes the self.items a query builder which makes look into the items table .By using this every time we call the JSON mathod we have to go into the table

    def __init__(self,name):
        self.name=name

    def json(self):
        return {'name':self.name,'items':[item.json() for item in self.items.all()]}

    # this function is used to search in database by name
    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() #select * from items where name=name limit 1

    # these are not the class method because they don't return the objects like find_by_name does
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
