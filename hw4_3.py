# -*- coding: utf-8 -*-
import threading
import time
import queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Cafe:
    def __init__(self, tables):
        self.tables = tables
        self.queue = queue.Queue()
        self.customer_number = 0

    def customer_arrival(self):
        while self.customer_number < 20:
            time.sleep(1)
            self.customer_number += 1
            print(f"Посетитель номер {self.customer_number} прибыл")
            self.serve_customer(self.customer_number)

    def serve_customer(self, customer_number):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f"Посетитель номер {customer_number} сел за стол {table.number} (начало обслуживания)")
                customer_thread = Customer(self, customer_number, table, self.queue) # передаю, не только клиента, но его стол и очередь кафе
                customer_thread.start()
                break
        else:
            print(f"Посетитель номер {customer_number} ожидает свободный стол (помещение в очередь)")
            self.queue.put(customer_number)

class Customer(threading.Thread):
    def __init__(self, cafe, customer_number, table, queue): # добавила объекты для передачи, чтобы легче было к ним обращаться
        super().__init__()
        self.cafe = cafe
        self.customer_number = customer_number
        self.table = table
        self.queue=queue

    def run(self): # немного переписала run с учетом того, что теперь получаем в ините, данный подход проще
        time.sleep(5)
        self.table.is_busy = False
        print(f'Посетитель {self.customer_number} поел и ушел')
        if not self.queue.empty():
            next_customer = self.queue.get()
            self.cafe.serve_customer(next_customer)



table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]
cafe = Cafe(tables)

customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

customer_arrival_thread.join()