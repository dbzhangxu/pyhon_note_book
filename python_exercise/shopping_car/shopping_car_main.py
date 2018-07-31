# -*- encoding: utf-8 -*-
import user_manager

goods = [
{"name": "电脑", "price": 1999},
{"name": "鼠标", "price": 10},
{"name": "游艇", "price": 20},
{"name": "美女", "price": 998}
]

#存储登录用户的信息，列表中的每一项为字典，字典的定义形式为{‘name’:{'passwd','account_money','shopping_car','bought_list'}}

# shopping_car_list存储用户选择的商品,但未付款，列表中字典的每一项的key包括：{name,price，num（购买数量）}
# bought_list存储用户已经购买的商品，列表中字典的每一项的key包括：{name,price，num（购买数量）}


def output_goods():
    for item in goods:
        print(str(goods.index(item)) + " " + item['name'] + " " + str(item['price']))


def output_user_goods_info(goods_list):
    for item in goods_list:
        print('\033[1;32;40m%s\033[0m' % "商品名称：%s     商品价格: %s    数量：%s" % (item['name'],str(item['price']),str(item['num'])))


def select_goods(user_name):
    output_goods()
    user_shopping_car_list = user_manager.user_info_dict[user_name]['user_shopping_car_list'] # 取出该用户的购物车商品列表
    selections = input("Please input seq num to choose goods and use space to spilt\n" + ">>>").strip().split(' ')
    #print('input "buy" is to pay and ')
    for selection in selections:
        try:
            good_name = goods[int(selection)]["name"]
            for shopping_car_item in user_shopping_car_list:
                #校验购物车中是否已经存在相同的商品，若相同，数量加1；否则，新增该商品
                if shopping_car_item['name'] == good_name:
                    shopping_car_item['num'] += 1
                    break
            else:
                user_shopping_car_list.append(
                    {'name':good_name,'price':goods[int(selection)]['price'],'num':1})
        except:
            print("No goods for Your choose %d " % (int(selection),))
    if len(user_shopping_car_list) != 0:
        print('\033[1;32;40m%s\033[0m' % "您购物车商品信息如下")
        output_user_goods_info(user_shopping_car_list)


def output_user_info(user_name):
    print("Your account info is the following\n" + '\033[1;32;40m%s\033[0m' % "Your account money is %s " % str(
        user_manager.user_info_dict[user_name]['account_money']))


def add_shopping_car_into_bought_list(user_name):
    for shopping_goods in user_manager.user_info_dict[user_name]['user_shopping_car_list']:
        for bought_item in user_manager.user_info_dict[user_name]['bought_list']:
            if bought_item['name'] == shopping_goods['name']:
                bought_item['num'] += shopping_goods['num']
                break
        else:
            user_manager.user_info_dict[user_name]['bought_list'].append(shopping_goods)

    # 付款后清空购物车
    user_manager.user_info_dict[user_name]['user_shopping_car_list'].clear()
    print('\033[1;32;40m%s\033[0m' % "付款成功")
    output_user_info(user_name)


def pay_goods(user_name):
    account_money = int(user_manager.user_info_dict[user_name]['account_money'])
    need_to_pay = 0

    shopping_car_list = user_manager.user_info_dict[user_name]['user_shopping_car_list']
    if len(shopping_car_list) == 0:
        print("购物车空空如也")
        return
    # 计算用户购物车中的商品总额
    for pay_item in shopping_car_list:
        need_to_pay += pay_item['price'] * pay_item['num']

    # 判断用户的余额是否充足购买购物车的商品
    if need_to_pay > account_money:
        print("Your account money is not enough to pay for the goods,Please adjust goods in your shopping car")

    else: # 余额充足，将用户的余额扣除，并将购物车中的商品添加到已购买的列表中
        account_money -= need_to_pay
        user_manager.user_info_dict[user_name]['account_money'] = account_money
        #add goods in shopping car into bought list
        add_shopping_car_into_bought_list(user_name)


def show_bought_list(user_name):
    bought_list = user_manager.user_info_dict[user_name]['bought_list']
    if len(bought_list) == 0:
        print("您尚未购买过任何商品")
    else:
        print('\033[1;32;40m%s\033[0m' % "您购买的商品清单如下：")
        output_user_goods_info(bought_list)


def go_shopping(user_name):
    print("welcome!" + " " + user_name)
    output_user_info(user_name)
    while True:
        cmd = input("Please input cmd for shopping\n" + "1:choose good and puts them into shopping_car\n" +
                    "2:pay for the goods\n" + "3:Query your paying record\n" + "4:Clear you empty\n" + "5:Exit\n" + ">>>")
        if cmd == '1':
            select_goods(user_name)
        elif cmd == '2':
            pay_goods(user_name)
        elif cmd == '3':
            show_bought_list(user_name)
        elif cmd == '4':
            user_manager.user_info_dict[user_name]['user_shopping_car_list'].clear()
        elif cmd == '5':
            print("See You!!!!")
            return
        else :
            print("Invalid cmd")


if __name__ == "__main__":
    user_manager.load_user_info()
    result, user_name = user_manager.access()
    if result:
        go_shopping(user_name)
    user_manager.store_user_info()