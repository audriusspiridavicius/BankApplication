from init import app,db
from database.model.bank import Bank
class DbOperations:

    @staticmethod
    def get_all(cls):
        with app.app_context():
            return cls.query.all()

    @staticmethod
    def save(data):
        with app.app_context():
            db.session.add(data)
            db.session.commit()

    @staticmethod
    def get_bank(id):
        with app.app_context():
            bank = Bank.query.get(id)
        return bank

if __name__ == '__main__':
    pass