from math import ceil

from scipy.optimize import fsolve

def calculate_installment(loan, annual_interest_rate, months):
    """
        formula A = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
        A - installment/вноска
        P - principal/главница
        r - interest/лихва
        n - months count/брой месеци
    """
    interest = (annual_interest_rate / 100) / 12
    installment = loan * (interest * (1 + interest) ** months) / ((1 + interest) ** months -1)

    return installment

def calculate_interest(loan_amount, num_payments, installment):
    # Усвояването е на един път като за лява част на уравнението се взема сумата на кредита
    D_l = [installment] * num_payments  # Месечни вноски (еднакви)
    S_l = [(l + 1) / 12 for l in range(num_payments)]  # Интервали за вноските в години (ежемесечно)

    # Функция за изчисление на сумите в уравнението
    def equation(x):
        right_sum = sum(D_l[j] * (1 + x) ** -S_l[j] for j in range(len(D_l)))
        return loan_amount - right_sum

    # Намиране на X чрез числен метод
    initial_guess = 0.05  # Начално предположение за X (5%)
    x_solution = fsolve(equation, initial_guess)[0]

    # Преобразуване на резултата в годишен процент
    annual_gpr_solution = x_solution * 100

    return annual_gpr_solution

def generate_payment_schedule(loan, annual_interest_rate, months):
    month_interest_rate = annual_interest_rate / 12 / 100 # Месечна лихва по кредита
    installment = calculate_installment(loan, annual_interest_rate, months) # Вноска по кредита
    principal = loan # Сума на кредита

    schedule = []

    for month in range(1, months + 1):
        interest_installment = round(principal * month_interest_rate, 2) # Вноска по лихва върху главницата
        principal_installment = round(installment - interest_installment, 2) # Вноска за погасяване по главницата
        principal -= principal_installment # Намаляне на главницата спрямо вноската за погасяване по главницата

        schedule.append({
            'month': month,
            'interest_installment': interest_installment,
            'principal_installment': principal_installment,
            'principal': principal
        })

    return schedule

def main():
    while True:
        choose_calculator = input(f'Изберете:\n[1] Калкулатор за вноска по кредит\n'
                                      '[2] Калкулатор за лихва по кредит\n'
                                      '[3] Генератор за погасителни вноски\n'
                                      '[4] Изход\nИзберете опция от 1 до 4: ')

        if choose_calculator == '4':
            break

        if not choose_calculator.isdigit() or int(choose_calculator) not in range(1, 4):
            print('\n##########################\n'
                  'Въведете цифра от 1 до 4!\n'
                  '##########################\n')
            continue

        if choose_calculator == '1':
            loan = float(input('Размер на кредита: '))
            annual_interest_rate = float(input('Процент лихва: '))
            months = int(input('Брой на вноските: '))
            installment = calculate_installment(loan, annual_interest_rate, months)
            total_loan = months * installment
            print(f'\n-----------------------------------------------------'
                  f'\nВноска: {installment:.2f}\nВърната сума в края на периода: {total_loan:.2f}\n'
                  f'-----------------------------------------------------\n')

        elif choose_calculator == '2':
            print('Въведете параметрите по кредита:')
            loan_amount = float(input('Размер на кредита: '))
            interest_payments = int(input('Брой на вноските: '))
            installment_amount = float(input('Размер на месечната вноска: '))
            annual_gpr_solution = calculate_interest(loan_amount, interest_payments, installment_amount)

            print(f'\n-----------------------------------------------------\n'
                  f'Годишният процент на разходите (ГПР) е: {annual_gpr_solution:.2f}%\n'
                  f'-----------------------------------------------------\n')

        elif choose_calculator == '3':
            loan = float(input('Размер на кредита: '))
            annual_interest_rate = float(input('Процент лихва: '))
            months = int(input('Брой на вноските: '))
            schedule = generate_payment_schedule(loan, annual_interest_rate, months)
            month_installment = calculate_installment(loan, annual_interest_rate, months)
            total_sum_of_loan = 0
            total_interest_paid = 0

            print('| {:^9} | {:^16} | {:^15} | {:^13} | {:^10} |'.format(
                'Вноска №', 'Вноска главница', 'Вноска лихва', 'Вноска общо', 'Главница'))
            print('-' * 79)

            for installment in schedule:
                print('| {:>9} | {:>16.2f} | {:>15.2f} | {:>13.2f} | {:>10.2f} |'.format(
                    installment['month'],
                    installment['principal_installment'],
                    installment['interest_installment'],
                    month_installment,
                    installment['principal']
                ))
                total_sum_of_loan += month_installment
                total_interest_paid += installment['interest_installment']

            print('-' * 79)
            print('| {:^16} | {:^15} |'.format(
                'Общо изплатено', 'Общо лихва'))
            print('| {:^16} | {:^15} |'.format(
                round(total_sum_of_loan, 2), round(total_interest_paid), 2))



if __name__ == "__main__":
    main()