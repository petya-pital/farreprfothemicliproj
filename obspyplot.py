# В файле вашего нового модуля, например, event_utils.py

from eventreader import * # Импорт вашего класса Event из основного модуля
import matplotlib.pyplot as plt
from obspy import Trace, Stream
def process_event(event):
    # Проверяем, что event является экземпляром класса Event
    if isinstance(event, Event):
        signal_data=event.signalData
        number_of_gauges, number_of_components = signal_data.shape
        for i in range(number_of_gauges-9):
            for j in range(number_of_components):
                data = signal_data[i,j].timeSeries
                trace = Trace(data=data)
                trace.stats.starttime = signal_data[i,j].timeDetected  # Начальное время
                trace.stats.sampling_rate = signal_data[i,j].ampl
                stream = Stream(traces=[trace])
                stream.plot()
                plt.show()

                # Ваш код для обработки объекта класса Event
        #print("Processing event:", event.header)
       # print("Catalog info:", event.catInfo)

        # Здесь вы можете добавить любую логику для обработки объекта event
    else:
        # Если event не является экземпляром класса Event, выведите сообщение об ошибке
        print("Error: Input is not an instance of Event class.")