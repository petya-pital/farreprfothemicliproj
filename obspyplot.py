    # # В файле вашего нового модуля, например, event_utils.py
    # from obspy.core import UTCDateTime
    # from eventreader import * # Импорт вашего класса Event из основного модуля
    # import matplotlib.pyplot as plt
    # from obspy.core import Trace, Stream
    # def drawSeismo(event, n=0, m=0):
    #     if isinstance(event, Event):
    #         if n == -1:
    #             signal_data = event.signalData
    #             number_of_gauges, number_of_components = signal_data.shape
    #             for i in range(number_of_gauges):
    #                 for j in range(number_of_components):
    #                     data = signal_data[i, j].timeSeries
    #                     trace = Trace(data=data)
    #                     print("Time detected:", signal_data[i, j].timeDetected)  # Отладочная информация
    #                     # Устанавливаем правильное время начала для каждого трейса
    #                     starttime = UTCDateTime(signal_data[i, j].timeDetected)
    #                     trace.stats.starttime = starttime
    #                     trace.stats.sampling_rate = signal_data[i, j].ampl
    #                     stream = Stream(traces=[trace])
    #                     stream.plot()
    #                     plt.show()
    #         else:
    #             signal_data = event.signalData
    #             data = signal_data[n, m].timeSeries
    #             trace = Trace(data=data)
    #             # Получаем относительное время
    #             relative_time = event.signalData[n, m].timeDetected
    #             # Устанавливаем начальное время для трассы
    #             trace.stats.starttime = relative_time
    #             trace.stats.sampling_rate = signal_data[n, m].ampl
    #             stream = Stream(traces=[trace])
    #             stream.plot()
    #             plt.show()
    #     else:
    #         print("Error: Input is not an instance of Event class.")
    #
    #
    #                 # Ваш код для обработки объекта класса Event
    #         #print("Processing event:", event.header)
    #        # print("Catalog info:", event.catInfo)
    #
    #         # Здесь вы можете добавить любую логику для обработки объекта event
from obspy.core import UTCDateTime
from obspy.core import Trace, Stream
import matplotlib.pyplot as plt
from eventreader import *

    # from obspy.core import UTCDateTime
    # from eventreader import * # Импорт вашего класса Event из основного модуля
    # import matplotlib.pyplot as plt
    # from obspy.core import Trace, Stream
def drawSeismo(event, n=0, m=0):
    if isinstance(event, Event):
        if n == -1:
            signal_data = event.signalData
            number_of_gauges, number_of_components = signal_data.shape
            for i in range(number_of_gauges):
                for j in range(number_of_components):
                    data = signal_data[i, j].timeSeries
                    trace = Trace(data=data)
                    relative_time = int(event.signalData[i, j].timeDetected)
                    #print(relative_time)
                    # Получаем абсолютное время начала для трассы, добавляя relative_time к event.UTCDate
                    starttime = UTCDateTime(event.UTCDate)  +  relative_time
                    trace.stats.starttime = starttime
                    print(starttime)
                    trace.stats.sampling_rate = signal_data[i, j].ampl
                    stream = Stream(traces=[trace])
                    stream.plot()
                    plt.show()
        else:
            signal_data = event.signalData
            data = signal_data[n, m].timeSeries
            trace = Trace(data=data)
            # Получаем относительное время
            relative_time = int(event.signalData[n, m].timeDetected)
            # Получаем абсолютное время начала для трассы, добавляя relative_time к event.UTCDate
            starttime = UTCDateTime(event.UTCDate) + relative_time  #+  relative_time_utc
            trace.stats.starttime = starttime
            trace.stats.sampling_rate = signal_data[n, m].ampl
            stream = Stream(traces=[trace])
            stream.plot()
            plt.show()
    else:
        print("Error: Input is not an instance of Event class.")
