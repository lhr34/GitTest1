# app/monitoring.py
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass

class DataProvider:
    def __init__(self):
        self.observers = []
        self.data_history = []

    def subscribe(self, observer: Observer):
        self.observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self.observers.remove(observer)

    def set_data(self, data):
        self.data_history.append(data)
        self.notify_all(data)

    def notify_all(self, data):
        for observer in self.observers:
            observer.update(data)

class DashboardDisplay(Observer):
    def update(self, data):
        # For demonstration, print to console
        print(f"[Dashboard] Current power consumption: {data} Watts")

class DataLogger(Observer):
    def __init__(self):
        self.log = []

    def update(self, data):
        self.log.append(data)
        print(f"[DataLogger] Data logged: {data} Watts")
