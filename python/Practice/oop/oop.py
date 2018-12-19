import datetime


class Account:
    """Simple account class with balance"""

    @staticmethod
    def _current_time():
        return datetime.datetime.now()

    def __init__(self, name, balance):
        self._name = name
        self._balance = balance
        self._transaction_list = [(Account._current_time(), self._balance)]
        print("Account created for " + self._name)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self.show_balance()
            self._transaction_list.append((Account._current_time(), amount))

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            self._transaction_list.append((Account._current_time(), - amount))

        else:
            print("You do no have a sufficient balance for this transaction")
        self.show_balance()

    def show_balance(self):
        print("Your current balance is: {}".format(self._balance))

    def show_transactions(self):
        for date, amount in self._transaction_list:
            if amount > 0:
                tran_type = "deposited"
            else:
                tran_type = "withdraw"
                amount *= -1
            print("{:6} {} on {})".format(amount, tran_type, date.astimezone()))


if __name__ == '__main__':
    tim = Account("Tim", 0)
    tim.deposit(1000)
    tim.withdraw(500)
    tim.show_transactions()

    print('*' * 40)

    steph = Account('Steph', 800)
    steph.deposit(100)
    steph.withdraw(200)
    steph.show_transactions()



