from db_setup import app

class DbOperations:

    @staticmethod
    def get_all(cls):

        with app.app_context():
            print(cls)
            print(type(cls))
            return cls.query.all()



if __name__ == '__main__':
    pass