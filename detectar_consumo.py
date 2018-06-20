#!/usr/bin/python2

from time import strftime, sleep, localtime
import threading
from os.path import expanduser


class DetectarConsumo():
    entrada = 0.0
    salida = 0.0
    total = 0.0
    interface = ""  # nombre de la interface a monotorear
    periodo = 0.0  # consumido en dicho periodo
    home = expanduser("~")

    def __init__(self, interface="eth0"):
        self.interface = interface
        self.calcular()

    def get_entrada(self):
        return self.entrada

    def get_salida(self):
        return self.salida

    def get_total(self):
        return self.total

    def get_periodo(self):
        return self.periodo

    def to_megabytes(self, numero=0.0):
        return numero/1024/1024

    def imprimir(*args):
        print(args)

    def calcular(self):
        total_anterior = self.total
        with open("/proc/net/dev", "r") as f:
            encontrado = False
            for linea in f.readlines():
                # f.seek(2, 1)
                linea_filtrada = linea.split()[0][:-1]  # para eliminar los : que viene despues de la interface
                if linea_filtrada == self.interface:
                    self.entrada = self.to_megabytes(float(linea.split()[1]))
                    self.salida = self.to_megabytes(float(linea.split()[9]))
                    self.total = self.entrada + self.salida
                    encontrado = True
                    break
            if not encontrado:
                print("no se encontro interface")
        self.periodo = self.total - total_anterior

    def ejecutar_dia(self):
        while True:
            if localtime().tm_hour == 0:
                self.calcular()
                self.escribirlog(archivo="consumo_dia.log",
                                 texto=strftime('%Y-%m-%d') +
                                 " " + str(self.entrada) +
                                 " " + str(self.salida) +
                                 " " + str(self.total) +
                                 " " + str(self.periodo) + "\n")
            sleep(3600)

    def ejecutar_hora(self):
        while True:
            if localtime().tm_min == 0:
                self.calcular()
                self.escribirlog(archivo="consumo_hora.log",
                                 texto=strftime('%Y-%b-%d %I %p') +
                                 " " + str(self.entrada) +
                                 " " + str(self.salida) +
                                 " " + str(self.total) +
                                 " " + str(self.periodo) + "\n")
            sleep(60)

    def ejecutar_minuto(self):
        while True:
            if localtime().tm_sec == 0:
                self.calcular()
                self.escribirlog(archivo="consumo_minuto.log",
                                 texto=strftime('%Y-%m-%d %H:%M') +
                                 " " + str(self.entrada) +
                                 " " + str(self.salida) +
                                 " " + str(self.total) +
                                 " " + str(self.periodo) + "\n")
            sleep(1)

    def detectarUptime(self):
        uptime = 0.0
        with open("/proc/uptime", "r") as f:
            uptime = float(f.readline().split()[0])
        return uptime

    def escribirlog(self, archivo="", texto=""):
        with open(self.home + "/log/" + archivo, "a") as f:
            f.write(texto)


interface = "enp2s0"

detectar_minuto = DetectarConsumo(interface)
detectar_hora = DetectarConsumo(interface)
detectar_dia = DetectarConsumo(interface)

hilo_minutos = threading.Thread(target=detectar_minuto.ejecutar_minuto)
hilo_horas = threading.Thread(target=detectar_hora.ejecutar_hora)
hilo_dias = threading.Thread(target=detectar_dia.ejecutar_dia)

hilo_minutos.start()
hilo_horas.start()
hilo_dias.start()
