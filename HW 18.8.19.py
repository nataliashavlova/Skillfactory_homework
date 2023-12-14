tickets_number = int(input("Введите количество билетов, которое вы хотите приобрести: "))
if tickets_number <= 0:
    print("Вы ввели неверное количество билетов")
else:
    ages_of_visitors = [int(input(f"Введите возраст посетителя {i}: ")) for i in range(1, tickets_number+1)]
    ticket_prices = [] #объявляем список, в который будут складываться стоимости билетов по условиям
    for a in range (tickets_number):
        if ages_of_visitors[a] < 18:
            ticket_prices.append(0)
        elif 18 <= ages_of_visitors[a] < 25:
            ticket_prices.append(990)
        elif ages_of_visitors[a] >=25:
            ticket_prices.append(1390)
    print("Сумма к оплате: "+str(sum(ticket_prices)) if tickets_number <= 3 \
          else ("Вам предоставлена скидка 10% за регистрацию более трех посетителей! Итого к оплате: "+str((sum(ticket_prices)-int(0.1*sum(ticket_prices))))))