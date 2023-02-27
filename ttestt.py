class One:
    """Класс частиц"""
    def __init__(self, name):
        self.name = name

    def display(self):
        return print('Имя: ' + self.name)
    
a = One('1')
b = a
b.name = '2'
One.display(a)
One.display(b)
 