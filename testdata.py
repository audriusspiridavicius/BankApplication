import random


from init import app, db
from database.model.bank import Bank
from database.model.person import Person
from database.model.bankaccount import BankAccount
def fill_accounts_table_test_data(number_of_records):
    list = []
    # User.query.with_entities(User.id).all()
    with app.app_context():
        bank_ids = Bank.query.with_entities(Bank.id).all()
        persons_ids = Person.query.with_entities(Person.id).all()

    b =[id[0] for id in bank_ids]
    p =[id[0] for id in persons_ids]

    for record in range(number_of_records):

        rand_bank = random.choice(b)
        rand_person = random.choice(p)

        with app.app_context():
            person = Person.query.get(rand_person)
            bank = Bank.query.get(rand_bank)



        r = BankAccount(account_number=random.randint(100000000, 999999999999),
                        person_id=random.choice(p),
                        bank_id=random.choice(b)
                        )
        # r = BankAccount(account_number=random.randint(100000000, 999999999999),
        #                 bank=bank,
        #                 person=person
        #                 )
        # r = BankAccount(account_number=random.randint(100000000, 999999999999))
        #
        # r.bank = bank
        # r.person = person
        list.append(r)
    with app.app_context():
        db.session.add_all(list)
        db.session.commit()

    print("fill_persons_table_test_data all good")

def fill_banks_table_test_data(number_of_records):

    banks = []

    for record in range(number_of_records):

        bank = Bank(name=f"bank{random.randint(100000,500000)}{record}",
                    address=f"test bank address{record}",
                    bank_code=f"test_123{random.randint(100000,500000)}45677{record}",
                    swift_code=f"test_swift_000{random.randint(100,1000)}123{record}",
                    )
        banks.append(bank)

    with app.app_context():
        db.session.add_all(banks)
        db.session.commit()
    print("fill_banks_table_test_data all good")


def fill_persons_table_test_data(number_of_records):

    persons = []

    for record_number in range(number_of_records):

        random_value = random.randint(0, 10000)

        person = Person(firstname=f"test name{random_value}",
                        lastname=f"test lastname{random_value}",
                        pin=f"00{random_value}{record_number}",
                        phone="860000000")
        persons.append(person)

    with app.app_context():
        db.session.add_all(persons)
        db.session.commit()

    print("fill_persons_table_test_data all good")




if __name__ == "__main__":

    # with app.app_context():
    #     # db.session.execute('delete from banksaccount')
    #     BankAccount.query.delete()
    #     db.session.commit()
    # fill_banks_table_test_data(10)
    # fill_persons_table_test_data(20)

    fill_accounts_table_test_data(10)
