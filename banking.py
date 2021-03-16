import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS card')
cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
cur.execute('SELECT * FROM card')
j = 0
conn.commit()
print(cur.fetchall())


class Account:
    def __init__(self):
        self.list_of_account = {}
        self.key = None
        self.pin = None
        self.balance = 0

    def new_account(self):
        self.key = "400000" + ''.join([str(random.randint(0, 9)) for _ in range(9)])
        odd = ([self.key[i] for i in range(len(self.key)) if i % 2 == 0])
        double_odd_c = ([int(i) * 2 for i in odd if int(i) * 2 < 10])
        c = sum(double_odd_c)  # double odd_cifre
        double_odd_n = ([int(i) * 2 - 9 for i in odd if int(i) * 2 >= 10])
        n = sum(double_odd_n)  # double odd_number
        p = sum([int(self.key[i]) for i in range(len(self.key)) if i % 2 != 0])  # par
        for i in range(0, 9):
            if (c + n + p + i) % 10 == 0:
                ck = i  # check_nr
                self.key = self.key + str(ck)
            else:
                cur.execute(f"DELETE FROM card WHERE number=({self.key});")
                conn.commit()

        self.pin = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        self.list_of_account[self.key] = self.key
        self.list_of_account[self.pin] = self.pin
        global j
        if len(self.key) == 16:
            j += 1
            cur.execute(f'INSERT INTO card (id, number, pin, balance) VALUES ({j}, {self.key}, {self.pin}, 0);')
            conn.commit()
            #print(len(self.key))
            return print(f"Your card has been created\nYour card number:\n{self.key}\nYour card PIN:\n{self.pin}\n")
        else:
            new.new_account()
    def luhn_check(self, cardNo):
        nDigits = len(cardNo)
        nSum = 0
        isSecond = False

        for i in range(nDigits - 1, -1, -1):
            d = ord(cardNo[i]) - ord('0')

            if (isSecond == True):
                d = d * 2

            # We add two digits to handle
            # cases that make two digits after
            # doubling
            nSum += d // 10
            nSum += d % 10

            isSecond = not isSecond

        if (nSum % 10 == 0):
            return True
        else:
            return False

    def if_exist(self, key_, pin_):
        cur.execute(f'SELECT number, pin FROM card WHERE number = {key_} and pin = {pin_}')
        existance = cur.fetchall()
        if not existance:
            return print("\nWrong card number or PIN!\n")
        else:
            return "You have successfully logged in!"

    def check_balance(self,key):
        cur.execute(f'SELECT balance FROM card WHERE number = {key}')
        data = cur.fetchone()
        return data[0]

    def enquiry_add_income(self,income, card_number):
        cur.execute(f"UPDATE card SET balance = balance + {income} WHERE number = {card_number};")
        conn.commit()
        return

    def enquiry_add_income1(self,income, card_number, pin):
        cur.execute(f"UPDATE card SET balance = balance + {income} WHERE number = {card_number} and pin = {pin};")
        conn.commit()
        return

    def enquiry_do_transfer(self, card_number, pin):
        card_input = input("Enter card number:\n")
        if not self.luhn_check(card_input):
            print("Probably you made a mistake in the card number.\nPlease try again!")
        else:
            cur.execute(f"SELECT number from card where number={card_input}")
            balance = cur.fetchone()
            if not balance:
                print("Such a card does not exist")
            else:
                transfer_money = int(input("Enter how much money you want to transfer:"))
                check_for_money = self.check_balance(card_number)
                if transfer_money > check_for_money:
                    print("Not enough money!")
                else:
                    self.enquiry_add_income(transfer_money, card_input)
                    cur.execute(f"UPDATE card SET balance = balance - {transfer_money} WHERE number = {card_number} and pin = {pin};")
                    conn.commit()
                    print("Success!")

    def enquiry_close_account(self, card_number, pin):
        cur.execute(f"DELETE FROM card WHERE number=({card_number}) and pin = {pin};")
        conn.commit()
        print("\nThe account has been closed!")

new = Account()
choice = None
while choice != 0:
    print("1. Create an account\n2. Log into account\n0. Exit\n")
    choice = int(input())
    if choice == 1:
        new.new_account()
    elif choice == 2:
        key = input("Enter your card number:\n")
        pin = input("Enter your PIN:\n")
        if (new.if_exist(key, pin)) == "You have successfully logged in!":
            print("\nYou have successfully logged in!")

            while True:
                print("\n1. Balance\n2. Add income\n" +
                      "3. Do transfer\n4. Close Acco" +
                      "unt\n5. Log out\n0. Exit\n")
                choice = int(input())
                if choice == 1:
                    bal = new.check_balance(key)
                    print("\nBalance: ",bal)
                if choice == 2:
                    print("\nEnter income:")
                    income = int(input())
                    new.enquiry_add_income1(income, key, pin)
                    print("Income was added!")
                if choice == 3:
                    print("\nTransfer")
                    new.enquiry_do_transfer(key,pin)
                if choice == 4:
                    new.enquiry_close_account(key,pin)
                if choice == 5:
                    print("You have successfully logged out!\n")
                if choice == 0:
                    print("Bye!")
                    break
                if choice == 4:
                    break
                if choice == 5:
                    break

    elif choice == 3:
        print("\nBye!")
        break
