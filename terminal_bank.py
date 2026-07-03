import json
import random
import string
from pathlib import Path


class bank:
    datapath = 'data.json'
    data=[]

    try:
          if Path(datapath).exists():
              with open(datapath) as fs:
               data=json.loads(fs.read())
          else:
              print("No such file exists: ")
          
    except Exception as err:
        print(f"An exception is occured:- {err}")

    @staticmethod
    def update():
        with open(bank.datapath, 'w') as fs:
            fs.write(json.dumps(bank.data))

    @classmethod
    def __generate(cls):
       return ''.join(random.choices(string.digits, k=12))

    def createaccount(self):

        data = {
            "Name": input("Enter your name:- "),
            "age": int(input("Enter your age")),
            "mail": input("Enter your email:- "),
            "phn" : int(input("Enter your mobile number:-")),
            "pin": int(input("Enter your pin")),
            "accoutn no." : bank.__generate() ,
            "balance": 0,
        }
        if data['age']<18:
            print("sorry you are not elligible to create an account:- ")
        elif len(str(data['pin']))!=4:
            print("Enter a 4 digit pin: ")
        elif len(str(data['phn']))!=10:
            print("Enter a 10 digit mobile no. ")
        else:
            print("Congratulation! your account has been succefully created: ")
            for i in data:
                print(f"{i} : {data[i]}") 
            print("pls Note your accoutn number: ")

            bank.data.append(data)
            bank.update()           
    
    def depositemoney(self):
        accno = (input("Enter your account number to deposite money: "))
        pin = int(input("Enter your pin: "))

        userdata= [i for i in bank.data if i['accoutn no.'] == accno and i['pin']== pin]

        if userdata == False:
            print("Sorry your account number is not found: ")
        
        else:
            amount = int(input("Enter amount to deposite: "))
            if amount >10000 or amount<0 :
                print("the amount is larger than 10k or below 0")
            else:
                userdata[0]['balance'] += amount
                bank.update()
                print("Your amount is deposited succesfully!")

    
    def withdrawmoney(self):
        accno = (input("Enter your account number to withdraw money: "))
        pin = int(input("Enter your pin: "))

        userdata= [i for i in bank.data if i['accoutn no.'] == accno and i['pin']== pin]

        if userdata == False:
            print("Sorry your account number is not found: ")
        
        else:
            amount = int(input("Enter amount to withdraw: "))
            if  userdata[0]['balance'] < amount  :
                print("youre not having sufficient amount to withdraw")
            else:
                userdata[0]['balance'] -= amount
                bank.update()
                print("Your amount is withdrawn succesfully!")

    def getdata(self):
        accno = (input("Enter your account number to get your details "))
        pin = int(input("Enter your pin: "))

        userdata= [i for i in bank.data if i['accoutn no.'] == accno and i['pin']== pin]
        print("your details are:- \n")
        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")
    

    def updatedetails(self):
        accno = (input("Enter your account number to update your details "))
        pin = int(input("Enter your pin: "))

        userdata= [i for i in bank.data if i['accoutn no.'] == accno and i['pin']== pin]

        if userdata == False:
            print("no such user found: ")
        else:
            print("you can change your name , mail , phn & pin")

        newdata = {
            "Name" : input("Enter your name or press enter to skip") ,
            "mail" : input("Enter your mail or press enter to skip"),
            "phn" : input("Enter your phn or press enter to skip"),
            "pin" : input("Enter your pin or press enter to skip")
        }    

        if newdata["Name"] == "" :
            newdata["Name"] = userdata[0]['Name']
        if newdata["mail"] == "" :
            newdata["mail"] = userdata[0]['mail']
        if newdata["phn"] == "" :
            newdata["phn"] = userdata[0]['phn']
        if newdata["pin"] == "" :
            newdata["pin"] = userdata[0]['pin']

        newdata['age'] = userdata[0]['age']
        newdata['accoutn no.'] = userdata[0]['accoutn no.']
        newdata['balance'] = userdata[0]['balance']

        if type(newdata['pin']) == str:
            newdata['pin'] = int(newdata['pin'])


        for i in newdata:
            if newdata[i] == userdata[0][i]:
                continue
            else:
                userdata[0][i] = newdata[i]    

        bank.update()
        print("Details updated succesfully! ")   
            
    
    def deletedetails(self):
        accno = (input("Enter your account number to update your details "))
        pin = int(input("Enter your pin: "))

        userdata= [i for i in bank.data if i['accoutn no.'] == accno and i['pin']== pin]

        if userdata == False:
            print("No such user found ")
        else:
            check = input("are you sure to delete your account? if yes press 'Y' if no press 'N'")

            if check == 'n' or check == 'N':
                pass
            else:
                index = bank.data.index(userdata[0])
                bank.data.pop(index)
            print("Account deleted succesfully!")

            bank.update()


user=bank()

print("Press 1 to open an creat an account")
print("Press 2 to deposite money in bank")
print("Press 3 to withdraw money")
print("Press 4 to get details")
print("Press 5 to update details")
print("Press 6 to delete your account")

check= int(input("Enter a valid number"))

if check== 1 :
    user.createaccount()

if check==2:
    user.depositemoney()

if check == 3:
    user.withdrawmoney()    

if check == 4:
    user.getdata()    

if check == 5:
    user.updatedetails()    

if check == 6:
    user.deletedetails()    