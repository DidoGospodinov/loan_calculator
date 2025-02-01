from datetime import datetime, date
from typing import List, Tuple
import math


class LoanCalculator:
    def __init__(self):
        self.DAYS_IN_YEAR = 365
        self.AVERAGE_MONTH = 30.41666  # 365/12

    def calculate_interest_rate(self,
                                loan_amount: float,
                                monthly_payment: float,
                                term_months: int) -> float:
        """
        Изчислява годишния лихвен процент при известни:
        - размер на кредита
        - месечна вноска
        - срок в месеци
        """
        tolerance = 0.0001
        max_iterations = 1000
        rate = 0.1  # Начално предположение 10%

        for _ in range(max_iterations):
            # Изчисляване на месечната вноска при текущия лихвен процент
            monthly_rate = rate / 12
            calculated_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** term_months) / (
                        (1 + monthly_rate) ** term_months - 1)

            # Проверка дали сме достигнали достатъчна точност
            if abs(calculated_payment - monthly_payment) < tolerance:
                break

            # Корекция на лихвения процент
            if calculated_payment > monthly_payment:
                rate *= 0.95
            else:
                rate *= 1.05

        return round(rate * 100, 2)

    def calculate_monthly_payment(self,
                                  loan_amount: float,
                                  annual_rate: float,
                                  term_months: int) -> float:
        """
        Изчислява месечна вноска при известни:
        - размер на кредита
        - годишен лихвен процент
        - срок в месеци
        """
        monthly_rate = annual_rate / 12 / 100
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** term_months) / (
                    (1 + monthly_rate) ** term_months - 1)
        return round(monthly_payment, 2)

    def calculate_loan_amount(self,
                              monthly_payment: float,
                              annual_rate: float,
                              term_months: int) -> float:
        """
        Изчислява размер на кредита при известни:
        - месечна вноска
        - годишен лихвен процент
        - срок в месеци
        """
        monthly_rate = annual_rate / 12 / 100
        loan_amount = monthly_payment * ((1 + monthly_rate) ** term_months - 1) / (
                    monthly_rate * (1 + monthly_rate) ** term_months)
        return round(loan_amount, 2)

    def generate_amortization_schedule(self,
                                       loan_amount: float,
                                       annual_rate: float,
                                       term_months: int,
                                       start_date: date = None) -> List[dict]:
        """
        Генерира погасителен план при зададени параметри
        """
        if start_date is None:
            start_date = date.today()

        monthly_rate = annual_rate / 12 / 100
        monthly_payment = self.calculate_monthly_payment(loan_amount, annual_rate, term_months)

        schedule = []
        remaining_balance = loan_amount

        for month in range(1, term_months + 1):
            interest_payment = remaining_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment

            payment_date = date(
                start_date.year + ((start_date.month + month - 1) // 12),
                ((start_date.month + month - 1) % 12) + 1,
                start_date.day
            )

            schedule.append({
                'payment_number': month,
                'payment_date': payment_date,
                'payment_amount': round(monthly_payment, 2),
                'principal': round(principal_payment, 2),
                'interest': round(interest_payment, 2),
                'remaining_balance': round(max(0, remaining_balance), 2)
            })

        return schedule


def main():
    calculator = LoanCalculator()

    while True:
        print("\nКалкулатор за кредити")
        print("1. Изчисляване на лихвен процент")
        print("2. Изчисляване на месечна вноска")
        print("3. Изчисляване на размер на кредит")
        print("4. Генериране на погасителен план")
        print("5. Изход")

        choice = input("\nИзберете опция (1-5): ")

        if choice == "1":
            loan_amount = float(input("Въведете размер на кредита: "))
            monthly_payment = float(input("Въведете месечна вноска: "))
            term_months = int(input("Въведете срок в месеци: "))

            rate = calculator.calculate_interest_rate(loan_amount, monthly_payment, term_months)
            print(f"\nГодишен лихвен процент: {rate}%")

        elif choice == "2":
            loan_amount = float(input("Въведете размер на кредита: "))
            annual_rate = float(input("Въведете годишен лихвен процент: "))
            term_months = int(input("Въведете срок в месеци: "))

            payment = calculator.calculate_monthly_payment(loan_amount, annual_rate, term_months)
            print(f"\nМесечна вноска: {payment:.2f}")

        elif choice == "3":
            monthly_payment = float(input("Въведете месечна вноска: "))
            annual_rate = float(input("Въведете годишен лихвен процент: "))
            term_months = int(input("Въведете срок в месеци: "))

            amount = calculator.calculate_loan_amount(monthly_payment, annual_rate, term_months)
            print(f"\nРазмер на кредита: {amount:.2f}")

        elif choice == "4":
            loan_amount = float(input("Въведете размер на кредита: "))
            annual_rate = float(input("Въведете годишен лихвен процент: "))
            term_months = int(input("Въведете срок в месеци: "))

            schedule = calculator.generate_amortization_schedule(loan_amount, annual_rate, term_months)
            print("\nПогасителен план:")
            for payment in schedule:
                print(f"Вноска {payment['payment_number']}: {payment['payment_amount']:.2f} "
                      f"(главница: {payment['principal']:.2f}, лихва: {payment['interest']:.2f}, "
                      f"оставащо: {payment['remaining_balance']:.2f})")

        elif choice == "5":
            break

        else:
            print("Невалиден избор. Моля, опитайте отново.")


if __name__ == "__main__":
    main()