# -*- encoding: utf-8 -*-
import json

goods = [
{"name": "电脑", "price": 1999},
{"name": "鼠标", "price": 10},
{"name": "游艇", "price": 20},
{"name": "美女", "price": 998}
]

#存储登录用户的信息，列表中的每一项为字典，字典的定义形式为{‘name’:{'passwd','account_money','shopping_car','bought_list'}}
user_info_dict = {}

# shopping_car_list存储用户选择的商品,但未付款，列表中字典的每一项的key包括：{name,price，num（购买数量）}
# bought_list存储用户已经购买的商品，列表中字典的每一项的key包括：{name,price，num（购买数量）}


def load_user_info(user_info_dict):
    try:
        with open("user_info.json",'r') as f:
            user_info_dict = json.load(f)
    except:
        print("No user info are stored")

def store_user_info(user_info_dict):
    try:
        with open("user_info.json",'w') as f:
            json.dump(user_info_dict,f)
    except:
        print("store user info failure")

def output_goods():
    for item in goods:
        print(str(goods.index(item)) + " " + item['name'] + " " + str(item['price']))


def select_goods(user_name):
    output_goods()
    user_shopping_car_list = user_info_dict[user_name]['user_shooping_car_list'] # 取出该用户的购物车商品列表

    seletions = input("Please input seq num to choose goods and use space to spilt").split(' ')
    print('input "buy" is to pay and ')
    for seletion in seletions:
        try:
            good_name = goods[seletion]["name"]
            for shopping_car_item in user_shopping_car_list:
                #校验购物车中是否已经存在相同的商品，若相同，数量加1；否则，新增该商品
                if shopping_car_item['name'] == good_name:
                    shopping_car_item['num'] += 1
                else:
                    shopping_car_item['name'] = good_name
                    shopping_car_item['price'] = goods[seletion]['price']
                    shopping_car_item['num'] = 1
            print('%s has been added to shopping car' % (good_name,))
        except:
            print("No selection good %d" % (seletion,))


def output_user_info(user_name):
    print("Your account info is the following\n" + "Your account money is " + str(
        user_info_dict[user_name]['account_money']) + '\n')


def pay_goods(user_name):
    account_money = user_info_dict[user_name]['account_money']
    need_to_pay = 0
    for pay_item in user_info_dict[user_name]['user_shooping_car_list']:
        need_to_pay += pay_item['price'] * pay_item['num']
    if need_to_pay > account_money:
        print("Your account money is not enough to pay for the goods,Please adjust goods in your shopping car")
    else:
        user_info_dict[user_name]['account_money'] -= need_to_pay
        #add goods in shopping car into bought list
        for shopping_goods in user_info_dict:
            pass

def go_shopping(user_name):
    print("welcome back!" + " " + user_name)
    output_user_info(user_name)
    while True:
        cmd = input("Please input cmd for shooping\n" + "1:choose good and puts them into shopping_car\n" +
                    "2:pay for the goods\n" + "3:Query your paying record")
        if cmd == '1':
            select_goods(user_name)
        elif cmd == '2':
            pay_goods(user_name)
        elif cmd == 3:
            print("See You!!!!")
            return


def check_passwd(user_name):
    count = 3
    while count > 0:
        passwd = input("please input your password\n" + "'q;' is exit")
        if passwd == user_info_dict[user_name]['passwd']:
            print("log success")
            return True
        else:
            count -= 1
            print("Passwd is not correct, left %d times\n" % (count,))
    else:
        return False


def login():
    while True:
        user_name = input("please input your user name\n" + "'q;' is exit")
        if user_name == '':
            print("please input again,your input is not correct\n")
        elif user_name == 'q;':
            return False
        else:
            #校验用户是否可以登录
            try:
                if not (user_name in user_info_dict.keys()):
                    print("your account is not exist,input again\n")
                    continue
                else:
                    if check_passwd():
                        return True
                    else:
                        print('passwd input error exceed 3 times,exit')
                        return False
            except:
                print("the user is not register")
                continue





def access():
    while True:
        cmd = input("Please input your choice\n"+"1 is login, 2 is register\n"+">>>")
        if cmd == '1':
            print("Your choice is login")
            return login()
        elif cmd == '2':
            print("Your choice is register")
            return register()
        elif cmd == 'q;':
            print("See You! O(∩_∩)O")
            return False
        else:
            print("your choice is not correct,please input again")

if __name__ == "__main__":
    output_goods()