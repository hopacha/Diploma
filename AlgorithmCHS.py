# -*- coding: utf-8 -*-
from matplotlib import pyplot
import time
import csv
pyplot.ion()
pyplot.show()
with open('RTSI.csv', 'rb') as csvfile:  #Открываем файл
    moex_data = csv.reader(csvfile)
    viborka = []  # Массив цен закрытия
    for row in moex_data:
        #a = int(row[7].replace('.',','))
        a = float(row[7])
        viborka.append(a)

#viborka.pop(0)   # удаляем заголовок столбца
#print viborka
csvfile.close()
pyplot.plot(viborka)
pyplot.draw()
time.sleep(10)
pyplot.ioff()
'''
obr_viborka = []
print viborkah
print max(viborka), min(viborka)
for row in viborka:
    obr_viborka.append((max(viborka)-row)/(row-(min(viborka)-0.00001)))

pyplot.plot(obr_viborka)
pyplot.draw()'''
#time.sleep(10)
#pyplot.ioff()

