import scrapy
import pandas as pd
import os
import matplotlib.pyplot as plt

# Определяем паука для сбора данных с сайта о полотенцесушителях
class TdnewparsSpider(scrapy.Spider):
    name = "tdnewpars"
    allowed_domains = ["tdom.info"]
    start_urls = ["https://tdom.info/santehnika/polotencesushiteli-i-komplektuyuschie"]

    def parse(self, response):
        # Получаем список всех товаров на странице
        towels = response.css("div.product-thumb")

        for towel in towels:
            # Извлекаем название товара
            name = towel.css("span.item-name::text").get()
            # Извлекаем цену товара
            price = towel.css("p.price::text").get()
            # Извлекаем ссылку на товар
            url = towel.css("div.caption a").attrib["href"]

            # Возвращаем собранную информацию в словаре
            yield {
                "Название товара": name.strip() if name else "Название отсутствует",
                "Цена товара": price.strip() if price else "Цена отсутствует",
                "Ссылка на товар": url if url else "URL отсутствует"
            }

    # Настройка экспорта в CSV с кодировкой UTF-8 с BOM для корректного отображения в Excel
    custom_settings = {
        'FEEDS': {
            'towels.csv': {
                'format': 'csv',
                'encoding': 'utf-8-sig',  # Используем 'utf-8-sig', чтобы добавить BOM
                'store_empty': False,
                'fields': ['Название товара', 'Цена товара', 'Ссылка на товар'],  # Указываем заголовки колонок
            },
        },
    }

# Функция для обработки CSV файла, вывода средней цены и построения гистограммы цен
def process_and_display_data(file_path):
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден. Убедитесь, что парсер успешно завершил работу.")
        return

    # Чтение файла CSV
    df = pd.read_csv(file_path)

    # Удаляем строки без цен и преобразуем столбец цен к числовому формату, удаляя символы валюты
    df['Цена товара'] = pd.to_numeric(df['Цена товара'].str.replace('[^\\d.]', '', regex=True), errors='coerce')
    df = df.dropna(subset=['Цена товара'])  # Удаляем строки с пустыми значениями цены

    # Вычисляем среднюю цену
    average_price = df['Цена товара'].mean()
    print(f"Средняя цена полотенцесушителя: {average_price:.2f} руб.")

    # Построение гистограммы цен
    plt.figure(figsize=(10, 6))
    plt.hist(df['Цена товара'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Гистограмма цен на полотенцесушители')
    plt.xlabel('Цена (руб.)')
    plt.ylabel('Количество')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Этот вызов следует выполнять после того, как Scrapy завершит свою работу
file_path = 'towels.csv'
process_and_display_data(file_path)
