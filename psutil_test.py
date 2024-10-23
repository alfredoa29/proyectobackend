import time

import psutil


#metodo que utiliza la libreria psutil para deolver el porcentaje de uso de cpu cada 1 segundo
def generate_cpu_usage():
    return psutil.cpu_percent(interval=1)

#metodo que utiliza la libreria psutil para devolver el porcentaje de uso de ram
def generate_ram_usage():
    return psutil.virtual_memory()[2]

#metodo que utiliza la libreria psutil para devolver el porcentaje de uso de memoria swap

def generate_swap_usage():
    return psutil.swap_memory().percent