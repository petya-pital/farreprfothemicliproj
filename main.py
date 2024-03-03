# This is a sample Python script.
import  eventreader as er
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import matplotlib.pyplot as plt
from obspy import Trace, Stream
import obspyplot
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
def has_date_in_header(header_json):
    return "'date\": \"" in header_json
def get_date_from_header(header_json):
    date_start = header_json.find("'date': '") + len("'date': '")
    date_end = header_json.find("'", date_start)
    date_str = header_json[date_start:date_end]
    time_start = header_json.find("'time': '") + len("'time': '")
    time_end = header_json.find("'", time_start)
    time_str = header_json[time_start:time_end]
    datetime_str = f"{date_str} {time_str}"
    return datetime_str
print(get_date_from_header(str(ev.catInfo)))

print((str(ev.catInfo)))
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
#plot_number_array(ev.signalData[0,0].timeSeries)
#signal_data = ev.signalData
#obspyplot.drawSeismo(ev,-1)
#print(signal_data)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
#number_of_gauges, number_of_components = signal_data.shape
#print("Количество датчиков:", number_of_gauges)
#print("Количество компонентов:", number_of_components)
#plot_number_array(ev.signalData[11,2].timeSeries)
#data = ev.signalData[11, 2].timeSeries
#trace = Trace(data=data)
#print(ev.catInfo.timeMine)
#trace.stats.starttime = 0.0  # Начальное время
#trace.stats.sampling_rate = 2000.0  # Частота дискретизации (например, 100 Гц)

# Создаем объект Stream и добавляем в него Trace
#stream = Stream(traces=[trace])

# Визуализируем данные
#stream.plot()
#plt.show()
#obspyplot.drawSeismo(ev,-1)
number_of_gauges, number_of_components = ev.signalData.shape
for i in range(number_of_gauges*number_of_components):
    a=i//3
    b=i%3
    print(ev.signalData[a,b].timeDetected)

obspyplot.drawSeismo(ev,2,2)