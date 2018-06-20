import threading
from time import sleep

def imprimir1():
    while True:
        print("1 segundo")
        sleep(1)


def imprimir2():
    while True:
        print("2 segundos")
        sleep(2)


def imprimir3():
    while True:
        print("3 segundos")
        sleep(3)


i1 = threading.Thread(target=imprimir1)
i2 = threading.Thread(target=imprimir2)
i3 = threading.Thread(target=imprimir3)

i1.start()
i2.start()
i3.start()
