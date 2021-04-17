#Coding:utf-8
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont, QColor
import sys
from random import randrange, choice


class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        # то, какие коэфециенты в шаблоне для рекурсии
        # [+-1, т.е. больше числа или меньше, когда есть рекурсия; чему кратно при проверке на рекурсию; чило, относительно которого всё происходит; слогаемое при нерекурсии; коэфициент при n^2 в формуле с рекурсией;
        # 5) коэфициент при n в формуле с рекурсией; слогаемое в формуле с рекурсией; коэфициент при рекурсии; слогаемое в рекурсии]
        self.variables = [1, 1, 10, 0, 0,
                          1, 1, 1, 1]
        # второй исход с рекурсивной формулой
        # [коэфициент при n^2 в формуле с рекурсией; коэфициент при n в формуле с рекурсией; слогаемое в формуле с рекурсией; коэфициент при рекурсии; слогаемое в рекурсии]
        self.variables2 = [0, 1, 1, 1, 1]
        self.whatcall = 10  # от чего вызываем
        self.answer = 0  # ответ на задачу
        # кнопка обновления
        self.updatebtn = QPushButton(self)
        self.updatebtn.clicked.connect(self.update)
        self.updatebtn.resize(50, 50)
        self.updatebtn.move(750, 550)
        self.updatebtn.setFont(QFont('Arial', 12))
        self.updatebtn.setText('ОБН')
        # лабел "ответ"
        self.anslab = QLabel(self)
        self.anslab.resize(150, 50)
        self.anslab.move(0, 550)
        self.anslab.setFont(QFont('Arial', 12))
        self.anslab.setText('ОТВЕТ:')
        # поле для ответа
        self.ansedit = QLineEdit(self)
        self.ansedit.resize(300, 50)
        self.ansedit.move(155, 550)
        self.ansedit.setFont(QFont('Arial', 12))
        # правильный ответ/нет лабел
        self.oklab = QLabel(self)
        self.oklab.resize(50, 50)
        self.oklab.move(460, 550)
        self.oklab.setFont(QFont('Arial', 12))
        self.oklab.setText('ДА')
        self.oklab.hide()
        # кнопка для проверки
        self.checkbtn = QPushButton(self)
        self.checkbtn.clicked.connect(self.checkAns)
        self.checkbtn.resize(150, 50)
        self.checkbtn.move(510, 550)
        self.checkbtn.setFont(QFont('Arial', 12))
        self.checkbtn.setText('ПРОВЕРИТЬ')
        # виджеты с условием на экране
        # [условие с =; возврвт с рекурсией; условие без =; возврат без рекурсии]
        self.tasklabs = []
        for i in range(7):
            self.tasklabs.append(QLabel(self))
            self.tasklabs[-1].resize(800, 50)
            self.tasklabs[-1].move(0, i * 55)
            self.tasklabs[-1].setFont(QFont('Ariel', 12))
            self.tasklabs[-1].show()
        self.update()
        
    def update(self):
        '''обновление задачи'''
        self.oklab.hide()  # скрытие лабела
        # рандомизация коэфициентов
        self.variables = [choice([-1, 1]), randrange(1, 4), randrange(1, 25), randrange(-5, 5), randrange(-5, 5),
                          randrange(-10, 5), randrange(-20, 20), choice(tuple(set(range(-5, 5)) - {0})), randrange(1, 5)]
        self.variables2 = [randrange(-5, 5), randrange(-10, 5), randrange(-20, 20), choice(tuple(set(range(-5, 5)) - {0})), randrange(1, 5)]
        if self.variables[0] == -1:
            self.whatcall = choice(range(self.variables[2] - 10, self.variables[2]))  # рандомизация аргумента
        else:
            self.whatcall = choice(range(self.variables[2] + 1, self.variables[2] + 11))  # рандомизация аргумента
        self.answer = self.getRec(self.whatcall)
        # заполняем лабел 0 (заголовок нерекурсии)
        s = 'При n <= ' + str(self.variables[2]) + ':'  # просто строка для промежуточного хранения текста
        if self.variables[0] == -1:
            s = s.replace('<', '>')
        self.tasklabs[0].setText(s)
        # заполняем лабел 1 (формула нерекурсии)
        s = 'F(n) = n '
        if self.variables[3] < 0:
            s = s + '- ' + str(-1 * self.variables[3])
        elif self.variables[3] > 0:
            s = s + '+ ' + str(self.variables[3])
        self.tasklabs[1].setText(s)
        # заполняем лабел 2 (заголовок рекурсии)
        s = 'При n > ' + str(self.variables[2])
        if self.variables[0] == -1:
            s = s.replace('>', '<')
        if self.variables[1] != 1:
            s = s + ' и кратно ' + str(self.variables[1])
        s = s + ':'
        self.tasklabs[2].setText(s)
        # заполняем лабел 3 (формула рекурсии)
        s = 'F(n) = '
        if self.variables[7] == 1:  # перед рекурсией
            s = s + 'F(n )'
        else:
            s = s + str(self.variables[7]) + 'F(n '
        if self.variables[0] == -1:  # слогаемое в рекурсии
            s = s + '+ ' + str(self.variables[8]) + ') '
        else:
            s = s + '- ' + str(self.variables[8]) + ') '
        if self.variables[4] == 1:  # n^2
            s = s + '+ ' + 'n^2 '
        elif self.variables[4] < 0:
            s = s + str(self.variables[4]) + 'n^2 '
        elif self.variables[4] > 0:
            s = s + '+' + str(self.variables[4]) + 'n^2 '
        if self.variables[5] == 1:  # n
            s = s + '+ ' + 'n'
        elif self.variables[5] < 0:
            s = s + str(self.variables[5]) + 'n '
        elif self.variables[5] > 0:
            s = s + '+' + str(self.variables[5]) + 'n '
        if self.variables[6] < 0:  # слогаемое
            s = s + str(self.variables[6])
        elif self.variables[6] > 0:
            s = s + '+' + str(self.variables[6])
        self.tasklabs[3].setText(s)  # запись на лабел
        # лабелы 4 и 5 (доп строки для кратности)
        if self.variables[1] == 1:
            self.tasklabs[4].setText('Чему равно F(' + str(self.whatcall) + ')?')
            self.tasklabs[5].setText('')
            self.tasklabs[6].setText('')
        else:
            self.tasklabs[4].setText('Иначе:')
            s = 'F(n) = '
            if self.variables2[3] == 1:  # перед рекурсией
                s = s + 'F(n )'
            else:
                s = s + str(self.variables2[3]) + 'F(n '
            if self.variables[0] == -1:  # слогаемое в рекурсии
                s = s + '+ ' + str(self.variables2[4]) + ') '
            else:
                s = s + '- ' + str(self.variables2[4]) + ') '
            if self.variables2[0] == 1:  # n^2
                s = s + '+ ' + 'n^2 '
            elif self.variables2[0] < 0:
                s = s + str(self.variables2[0]) + 'n^2 '
            elif self.variables2[0] > 0:
                s = s + '+' + str(self.variables2[0]) + 'n^2 '
            if self.variables2[1] == 1:  # n
                s = s + '+ ' + 'n'
            elif self.variables2[0] < 0:
                s = s + str(self.variables2[0]) + 'n '
            elif self.variables2[0] > 0:
                s = s + '+' + str(self.variables2[0]) + 'n '
            if self.variables2[2] < 0:  # слогаемое
                s = s + str(self.variables2[2])
            elif self.variables2[2] > 0:
                s = s + '+' + str(self.variables2[2])
            self.tasklabs[5].setText(s)  # запись на лабел
            self.tasklabs[6].setText('Чему равно F(' + str(self.whatcall) + ')?')

        
    def getRec(self, whatcall):
        '''возвращает, что должно быть в результате рекурсии'''
        if self.variables[0] == 1 and whatcall <= self.variables[2] or\
           self.variables[0] == -1 and whatcall >= self.variables[2]:  # возвращается не рекурсия
            return whatcall + self.variables[3]
        elif (self.variables[0] == 1 and whatcall > self.variables[2] or\
           self.variables[0] == -1 and whatcall < self.variables[2]) and whatcall % self.variables[1] == 0:  # возвращается рекурсия при кратном
            return self.variables[7] * self.getRec(whatcall - self.variables[0] * self.variables[8]) + self.variables[4] * whatcall ** 2 +\
                   whatcall * self.variables[5] + self.variables[6]
        else:  # возврвщает при некратном
            return self.variables2[3] * self.getRec(whatcall - self.variables[0] * self.variables2[4]) + self.variables2[0] * whatcall ** 2 +\
                   whatcall * self.variables2[1] + self.variables[2]

    def checkAns(self):
        try:
            ans = int(self.ansedit.text())
            self.oklab.show()
            if ans == self.answer:
                self.oklab.setText('<p style="color: rgb(10, 155, 10); font-size: 12 px;">ДА</p>')
            else:
                self.oklab.setText('<p style="color: rgb(250, 10, 10); font-size: 12 px;">НЕТ</p>')
        except:
            self.oklab.setText('<h1 style="color: rgb(250, 10, 10); font-size: 12 px;">ERR,</h1>')
        print(self.answer)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MW()
    mw.show()
    sys.exit(app.exec_())
    
