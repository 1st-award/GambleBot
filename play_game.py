import random

def roll_dice():
    dice= []
    for i in range(0, 5):
        temp= random.randint(1, 7)
        dice.append(temp)

    return str(dice)

def clean_str(temp, cnt):
    temp = str(temp).strip('[]')
    temp = temp.replace("'", "", cnt)

    return temp

def select(x):
    return {'1': '1을 선택하셨습니다.', 'b': '2를 선택하셨습니다.'}.get(x, '3')
