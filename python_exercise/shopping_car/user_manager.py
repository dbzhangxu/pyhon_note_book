# -*- encoding: utf-8 -*-

import json
user_info_dict = {}


def login():
    while True:
        user_name = input("please input your user name, quit is exit\n" + ">>>")
        if user_name == '':
            print("please input again,your input is not correct\n")
        elif user_name == 'quit':
            return False,''
        else:
            #校验用户是否可以登录
            try:
                if not (user_name in user_info_dict.keys()):
                    print("your account is not exist,input again\n")
                    continue
                else:
                    if check_passwd(user_name):
                        return (True,user_name)
                    else:
                        print('passwd input error exceed 3 times,exit')
                        return False,''
            except:
                print("the user is not register")
                continue


def check_account_money(account_money):
    if account_money.isdigit():
        return True
    else:
        print("Your account money is error ,input again")
        return False


def register():
    while True:
        user_input = input("please input your user_name,user_passwd,account_money. Using SPACE split ,quit is exit \n" + ">>>")
        input_list = user_input.split(' ')
        try:
            if input_list[0] == 'quit':
                return False,''
            else:
                user_name,user_passwd ,account_money = input_list
                if check_passwd(user_name,user_passwd,False) and check_account_money(account_money):
                    user_info_dict[user_name] = {'passwd':user_passwd,'account_money':account_money,
                                                 'user_shopping_car_list':[],'bought_list':[]}
                    return True,user_name
                else :
                    continue
        except:
            print("input is error ,input again")


def access():
    while True:
        cmd = input("Please input your choice\n"+"1 is login, 2 is register\n"+">>>")
        if cmd == '1':
            print("Your choice is login")
            return login()
        elif cmd == '2':
            print("Your choice is register")
            return register()
        elif cmd == 'q':
            print("See You! O(∩_∩)O")
            return False,False
        else:
            print("Invalid cmd,input again")


def check_passwd(user_name,user_passwd = '',is_log_in = True):
    if is_log_in:
        count = 3
        while count > 0:
            passwd = input("please input your password\n" + ">>>")
            if passwd == user_info_dict[user_name]['passwd']:
                print("log success")
                return True
            else:
                count -= 1
                print("Passwd is not correct, left %d times\n" % (count,))
        else:
            return False
    else:# 注册用户，校验输入合法性
        if user_name in user_info_dict.keys():
            print("Your user_name is exist")
            return False
        else:
            if user_passwd == '':
                print("passwd should not be empty,input again")
                return False
        return True


def load_user_info():
    try:
        with open("user_info.json",'r') as f:
            global user_info_dict
            user_info_dict = json.load(f)
    except:
        print("No user info are stored")


def store_user_info():
    try:
        with open("user_info.json",'w') as f:
            json.dump(user_info_dict,f)
    except:
        print("store user info failure")