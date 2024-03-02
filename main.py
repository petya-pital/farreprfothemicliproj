# This is a sample Python script.
import  eventreader as er
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import matplotlib.pyplot as plt
from obspy import Trace, Stream

def plot_number_array(data):
    plt.plot(data)
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title("Number Array Plot")
    plt.grid(True)
    plt.show()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
def load_file_as_byte_array(file_path):
    with open(file_path, "rb") as file:
        byte_array = file.read()
    return byte_array
f = load_file_as_byte_array("Documents/Событие_30_11_2022__03-18-59_ID173232.event")
ev = er.try_read(f)
print(ev.catInfo)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
plot_number_array(ev.signalData[0,0])
signal_data = ev.signalData

print(signal_data)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
number_of_gauges, number_of_components = signal_data.shape
print("Количество датчиков:", number_of_gauges)
print("Количество компонентов:", number_of_components)
plot_number_array(ev.signalData[11,2])
data = ev.signalData[11, 2]
trace = Trace(data=data)
#print(ev.catInfo.timeMine)
trace.stats.starttime = 0.0  # Начальное время
trace.stats.sampling_rate = 2000.0  # Частота дискретизации (например, 100 Гц)

# Создаем объект Stream и добавляем в него Trace
stream = Stream(traces=[trace])

# Визуализируем данные
stream.plot()
plt.show()