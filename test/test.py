# guess number game
import random


def guess():
    print('game start...')  # 提示游戏开始
    rightnum = random.randint(1, 100)  # 生成随机数
    inputtime = 7  # 定义初始次数共7次，7次猜错就结束
    beginnum = 1  # 数字范围开头为1，结尾为100，判断大小之后用输入的数字代替开头或结尾
    endnum = 100

    # while循环递减次数  次数为0 结束循环  或者猜对了也结束循环
    while inputtime > 0:
        inputnum = int(input('请输入你猜的数字：'))
        # 如果猜对了  游戏就结束了  这个时候弹出对话框是否再来一次
        if rightnum == inputnum:
            print('YOU WIN !')
            choice = input('再来一次？ Y OR N')
            # 这个while True循环，只有在输入不是Y也不是N的情况下让用户无限次重新输入
            # 直到Y或者N时，通过return和break都可以跳出循环
            while True:
                if choice == 'Y' or choice == 'y':
                    return guess()
                elif choice == 'N' or choice == 'n':
                    break
                else:
                    choice = input('输入不正确，请重新输入 Y or N')
                    continue

        elif inputnum > rightnum:
            print("High")
            endnum = inputnum
            inputtime -= 1
            print(beginnum, endnum, '还剩次数：', inputtime)
            continue
        elif inputnum < rightnum:
            print("Low")
            beginnum = inputnum
            inputtime -= 1
            print(beginnum, endnum, '还剩次数：', inputtime)
            continue
        else:
            print("输入错误，请重新输入")
            continue


    else:
        print('game over')
        print('正确数字是：' + str(rightnum))
        choice = input('再来一次？ Y OR N')
        while True:
            if choice == 'Y' or choice == 'y':
                return guess()
            elif choice == 'N' or choice == 'n':
                break
            else:
                choice = input('输入不正确，请重新输入 Y or N')
                continue


guess()
