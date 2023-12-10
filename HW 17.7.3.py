per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}
money = int(input("Введите сумму в рублях, которую хотели бы положить на вклад:"))
deposit = list(map(int, [money+money*per_cent['ТКБ']/100,
           money+money*per_cent['СКБ']/100,
           money+money*per_cent['ВТБ']/100,
           money+money*per_cent['СБЕР']/100]))

print ("Максимальная сумма, которую вы можете заработать за год -", max(deposit)-money, "руб")