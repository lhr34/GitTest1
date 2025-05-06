from abc import ABC, abstractmethod

# Abstract Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, data):
        # Must be implemented by concrete observers to receive updates
        pass

# Subject class that provides data to observers
class DataProvider:
    def __init__(self):
        self.observers = []      # List of all subscribed observers
        self.data_history = []   # Historical log of all data updates

    def subscribe(self, observer: Observer):
        # Add an observer to the list
        self.observers.append(observer)

    def unsubscribe(self, observer: Observer):
        # Remove an observer from the list
        self.observers.remove(observer)

    def set_data(self, data):
        # Add new data to history and notify all observers
        self.data_history.append(data)
        self.notify_all(data)

    def notify_all(self, data):
        # Notify each observer by calling its update() method
        for observer in self.observers:
            observer.update(data)

# Concrete Observer: displays data on dashboard
class DashboardDisplay(Observer):
    def update(self, data):
        # Format and display sensor data for visualization
        print(f"[Dashboard] Sensor Date - "
              f"Power: {data['PowerSensor']}W | "
              f"Temperature: {data['TemperatureSensor']}°C | "
              f"Humidity: {data['HumiditySensor']}% | "
              f"Light: {data['LightSensor']}lux")

# Concrete Observer: logs data for historical analysis or storage
class DataLogger(Observer):
    def __init__(self):
        self.log = []  # Internal log list to store all received data

    def update(self, data):
        # Print and (optionally) log the received data
        print(f"[DataLogger] 记录完整数据: {data}")
        # self.log.append(data)  # Could store for later use
