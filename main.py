import json
import sys
import urllib.error
import urllib.request


API_URL = "https://open.er-api.com/v6/latest/"


COMMON_CURRENCIES = {
    "USD": "доллар США",
    "EUR": "евро",
    "RUB": "российский рубль",
    "GBP": "британский фунт",
    "CNY": "китайский юань",
    "JPY": "японская иена",
    "KZT": "казахстанский тенге",
    "TRY": "турецкая лира",
    "AED": "дирхам ОАЭ",
    "BYN": "белорусский рубль",
}


def load_rates(base_currency):
    """Получает актуальные курсы валют из открытого API."""
    url = API_URL + base_currency

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read().decode("utf-8")
    except urllib.error.URLError:
        raise RuntimeError("Не удалось подключиться к сервису курсов валют.")

    try:
        parsed = json.loads(data)
    except json.JSONDecodeError:
        raise RuntimeError("Сервис вернул данные в неизвестном формате.")

    if parsed.get("result") != "success":
        raise RuntimeError("Не удалось получить курс для выбранной валюты.")

    return parsed


def ask_currency(prompt):
    currency = input(prompt).strip().upper()
    if len(currency) != 3 or not currency.isalpha():
        raise ValueError("Код валюты должен состоять из 3 латинских букв, например USD.")
    return currency


def ask_amount():
    raw_amount = input("Введите сумму: ").strip().replace(",", ".")
    try:
        amount = float(raw_amount)
    except ValueError:
        raise ValueError("Сумма должна быть числом.")

    if amount <= 0:
        raise ValueError("Сумма должна быть больше нуля.")

    return amount


def show_common_currencies():
    print("\nПопулярные валюты:")
    for code, name in COMMON_CURRENCIES.items():
        print(f"{code} - {name}")


def convert_currency():
    show_common_currencies()
    print("\nПример ввода: USD, EUR, RUB")

    amount = ask_amount()
    from_currency = ask_currency("Из какой валюты переводим: ")
    to_currency = ask_currency("В какую валюту переводим: ")

    if from_currency == to_currency:
        print(f"\nРезультат: {amount:.2f} {to_currency}")
        return

    data = load_rates(from_currency)
    rates = data["rates"]

    if to_currency not in rates:
        raise ValueError("Такой валюты нет в списке доступных курсов.")

    rate = rates[to_currency]
    result = amount * rate

    print("\nРезультат конвертации:")
    print(f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}")
    print(f"Курс: 1 {from_currency} = {rate:.4f} {to_currency}")
    print(f"Дата обновления курса: {data.get('time_last_update_utc', 'не указана')}")


def main():
    print("Конвертер валют с актуальным курсом")
    print("-----------------------------------")

    while True:
        print("\nМеню:")
        print("1 - Конвертировать валюту")
        print("2 - Показать популярные валюты")
        print("0 - Выход")

        choice = input("Выберите пункт меню: ").strip()

        try:
            if choice == "1":
                convert_currency()
            elif choice == "2":
                show_common_currencies()
            elif choice == "0":
                print("Программа завершена.")
                break
            else:
                print("Такого пункта меню нет.")
        except (ValueError, RuntimeError) as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
        sys.exit(0)
