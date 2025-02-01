from bs4 import BeautifulSoup

def concatenate_html_files(file1_path, file2_path, output_path):
    try:
        with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
            html1 = f1.read()
            html2 = f2.read()

        soup1 = BeautifulSoup(html1, 'html.parser')
        soup2 = BeautifulSoup(html2, 'html.parser')

        body1 = soup1.body
        body2 = soup2.body

        if body1 and body2:
            # Перебираем дочерние элементы <body> второго файла и добавляем их в <body> первого
            for child in body2.contents:
                body1.append(child)

            # Сохраняем измененный soup1 в новый файл
            with open(output_path, 'w', encoding='utf-8') as outfile:
                outfile.write(soup1.prettify(encoding='utf-8').decode('utf-8')) # prettify для форматирования, decode для строки
            print(f"HTML файлы успешно склеены и сохранены в {output_path}")
        else:
            print("Не удалось найти теги <body> в одном или обоих файлах.")

    except FileNotFoundError:
        print("Один или оба файла не найдены.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования:
file1_path = 'messages.html'  # Замените на путь к вашему первому файлу
file2_path = 'messages2.html'  # Замените на путь к вашему второму файлу
output_path = 'combined.html' # Путь для сохранения результата

concatenate_html_files(file1_path, file2_path, output_path)