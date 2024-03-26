import re
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя\n'
with open("output.txt", "r", encoding="utf-8", errors="ignore") as file:
    text = file.read()

text = text.replace('А', 'а').replace('Б', 'б').replace('В', 'в').replace('Г', 'г').replace('Д', 'д').replace('Е', 'е').replace('Ё', 'ё').replace('Ж', 'ж').replace('З', 'з').replace('И', 'и').replace('Й', 'й').replace('К', 'к').replace('Л', 'л').replace('М', 'м').replace('Н', 'н').replace('О', 'о').replace('П', 'п').replace('Р', 'р').replace('С', 'с').replace('Т', 'т').replace('У', 'у').replace('Ф', 'ф').replace('Х', 'х').replace('Ц', 'ц').replace('Ч', 'ч').replace('Ш', 'ш').replace('Щ', 'щ').replace('Ъ', 'ъ').replace('Ы', 'ы').replace('Ь', 'ь').replace('Э', 'э').replace('Ю', 'ю').replace('Я', 'я')
regex = re.compile('[^%s]' % alphabet)
text = regex.sub('', text)
with open("output2.txt", "w", encoding="utf-8") as file:
    file.write(text)
