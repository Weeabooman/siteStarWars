class SWCodeConverter:
    regex = r'SW-\d+'   # строка вида SW-число

    def to_python(self, value):
        return value  # преобразование в Python-объект (можно доп. обработку)

    def to_url(self, value):
        return value  # обратно в строку для URL