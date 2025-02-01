import re
import csv
from collections import defaultdict
from bs4 import BeautifulSoup

with open(r'combined.html', 'r', encoding='utf-8') as f1:
    html = f1.read()
    soup = BeautifulSoup(html, 'html.parser')

    messages_data = []
    reaction_counts = defaultdict(int)

    for message_div in soup.find_all('div', class_='message default clearfix'):
        
        date_element = message_div.find('div', class_='pull_right date details')
        if date_element:
            date_time = date_element.get('title')
        else:
           date_time = None
        
        body = message_div.find('div', class_='body')
        if body:
            message = body.find(class_='text')

            if message:
                message_text = message.get_text(strip=True)

                # Поиск и удаление смайлика и "У тебя новое анонимное сообщение!" в начале
                message_text = re.sub(r'^[^\s]*\s*У тебя новое анонимное сообщение!\s*', '', message_text)

                # Поиск и удаление "↩️ Свайпни для ответа." в конце
                message_text = re.sub(r'\s*↩️\s*Свайпни для ответа\.\s*$', '', message_text)
            else:
                message_text = None
        else:
           message_text = None

        reactions = message_div.find(class_='reactions')
        reaction_data = []
        if reactions:
            for reaction_div in reactions.find_all(class_='reaction'):
                emoji = reaction_div.find(class_='emoji')
                count = reaction_div.find(class_='count')

                if emoji and count:
                    emoji_text = emoji.get_text(strip=True)
                    count_num = int(count.get_text(strip=True))
                    reaction_data.append({"emoji": emoji_text, "count": count_num})
                    reaction_counts[emoji_text] += count_num

        messages_data.append({"date_time": date_time, "message": message_text, "reactions": reaction_data})

    # Запись в CSV файл для сообщений
    with open('messages.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Date', 'Message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in messages_data:
            writer.writerow({'Date': item['date_time'], 'Message': item['message']})

    # Запись в CSV файл для реакций
    with open('reactions.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Reaction', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for emoji, count in reaction_counts.items():
            writer.writerow({'Reaction': emoji, 'Count': count})


    # Вывод статистики по реакциям
    print("Статистика по реакциям:")
    for emoji, count in reaction_counts.items():
        print(f"{emoji}: {count}")
    
    print("Данные сообщений сохранены в messages.csv")
    print("Данные по реакциям сохранены в reactions.csv")