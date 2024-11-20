import dis

class Calculator:
    def add(self, x, y):
        return x + y
    
    def subtract(self, x, y):
        return x - y
    
    def multiply(self, x, y):
        return x * y
    
    def divide(self, x, y):
        if y == 0:
            raise ValueError("Деление на ноль невозможно!")
        return x / y
    
    def power(self, x, y):
        return x ** y
    
def main():
    calc = Calculator()
    while True:
        print("\nКалькулятор")
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")
        print("4. Деление")
        print("5. Возведение в степень")
        print("6. Выход")
        
        choice = input("Выберите операцию (1-6): ")
        
        if choice == '6':
            print("До свидания!")
            break
        
        if choice in ('1', '2', '3', '4', '5'):
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))
            
            if choice == '1':
                print(f"Результат: {calc.add(num1, num2)}")
            elif choice == '2':
                print(f"Результат: {calc.subtract(num1, num2)}")
            elif choice == '3':
                print(f"Результат: {calc.multiply(num1, num2)}")
            elif choice == '4':
                try:
                    print(f"Результат: {calc.divide(num1, num2)}")
                except ValueError as e:
                    print(f"Ошибка: {e}")
            elif choice == '5':
                print(f"Результат: {calc.power(num1, num2)}")
        else:
            print("Неверный выбор!")

# Анализ байт-кода для каждого метода
print("\n=== Анализ байт-кода метода add ===")
dis.dis(Calculator.add)

print("\n=== Анализ байт-кода метода subtract ===")
dis.dis(Calculator.subtract)

print("\n=== Анализ байт-кода метода multiply ===")
dis.dis(Calculator.multiply)

print("\n=== Анализ байт-кода метода divide ===")
dis.dis(Calculator.divide)

print("\n=== Анализ байт-кода метода power ===")
dis.dis(Calculator.power)

print("\n=== Анализ байт-кода функции main ===")
dis.dis(main)

if __name__ == "__main__":
    main()
