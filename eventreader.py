import json
import zipfile
import io
import struct
import numpy as np
from datetime import datetime, timedelta
import  re

class Event:
    NUMBER_OF_COMPONENTS = 3

    def __init__(self):
        self.header = ""
        self.catInfo = CatalogInfo()
        self.signalData = None  # Заменяем self.signalData.timeSeries на self.signalData
        self.UTCDate = None  # Добавляем поле для хранения времени в формате UTC

    @property
    def numberOfChannels(self):
        return self.signalData.shape[0] * Event.NUMBER_OF_COMPONENTS


class SignalData:
    def __init__(self):
        self.timeSeries = None
        self.ampl = 200.0
        self.timeDetected = 0.0
class Datchik:
    def __init__(self):
        self.Introduction = False
        self.IntroID = 0


class EventType:
    def __init__(self):
        self.alias = ""


class CatalogInfo:
    def __init__(self):
        self.etype = EventType()
        self.timeMine = ""
        self.E = 0.0


class Header:
    def __init__(self):
        self.datchiki = []


def unzip_mem(zipped_buffer):
    with zipfile.ZipFile(io.BytesIO(zipped_buffer)) as archive:
        entry = archive.infolist()[0]
        with archive.open(entry) as unzipped_entry_stream:
            return unzipped_entry_stream.read()


def string_from_bytes_a(data, offset):
    str_size = int.from_bytes(data[offset:offset + 4], byteorder='little')
    offset += 4
    str_bytes = data[offset:offset + str_size]
    offset += str_size
    return str_bytes.decode('cp1251'), offset


def init_signal_data_array(number_of_gauges, number_of_samples=0):
    signal_data = np.empty((number_of_gauges, Event.NUMBER_OF_COMPONENTS), dtype=object)
    for m in range(number_of_gauges):
        for l in range(Event.NUMBER_OF_COMPONENTS):
            signal_data[m, l] = SignalData()  # Инициализируем новый объект SignalData для каждого элемента
            signal_data[m, l].timeSeries = None if number_of_samples == 0 else np.zeros(number_of_samples, dtype=np.float32)
    return signal_data


def get_number_of_gauges(header_json):
    hm = json.loads(header_json)
    return len(hm['datchiki'])


def get_cat_info(cat_json):
    return json.loads(cat_json)


def get_date_from_header(header_json):
    date_start = header_json.find('"date": "') + len('"date": "')
    date_end = header_json.find('"', date_start)
    date_str = header_json[date_start:date_end]

    time_start = header_json.find('"time": "') + len('"time": "')
    time_end = header_json.find('"', time_start)
    time_str = header_json[time_start:time_end]

    datetime_str = f"{date_str} {time_str}"

    # Преобразование строки в объект datetime
    datetime_obj = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M:%S')

    # Конвертация в формат UTC
    utc_datetime = datetime_obj - timedelta(hours=7)  # Предполагая, что ваш часовой пояс UTC+7
    return utc_datetime
def get_introID(header_json):
    intro_ids = []
    start_index = header_json.find('"IntroID":')
    while start_index != -1:
        start_index += len('"IntroID":')
        end_index = header_json.find(',', start_index)
        intro_id = int(header_json[start_index:end_index].strip())
        intro_ids.append(intro_id)
        start_index = header_json.find('"IntroID":', end_index)
    return intro_ids
def try_read(db_data):
    MODERN_DBID = 2718281828459045
    orig_db_data_offset = 0
    version_id = struct.unpack_from('q', db_data, orig_db_data_offset)[0]
    orig_db_data_offset += struct.calcsize('q')

    if version_id == MODERN_DBID:
        zipped = db_data[orig_db_data_offset:]
        data = unzip_mem(zipped)
        offset = 0

        header_json, offset = string_from_bytes_a(data, offset)
        print('date' in str(header_json))
#        print(get_date_from_header(header_json))
        print(get_introID(header_json))
        #print(header_json)
        print('sss \n')
        db_rec_json, offset = string_from_bytes_a(data, offset)
      #  print( db_rec_json)
        seis_rec_json = ""
        if data[offset] == 1:  # if event is processed
            offset += 1
            seis_rec_json, offset = string_from_bytes_a(data, offset)
           # print(seis_rec_json)
            print('sss \n')
        NUMBER_OF_GAUGES = get_number_of_gauges(header_json)
        NUMBER_OF_CHANNELS = NUMBER_OF_GAUGES * Event.NUMBER_OF_COMPONENTS
        sample_length = (len(data) - offset) // (struct.calcsize('h') * NUMBER_OF_CHANNELS)
        signal_data = init_signal_data_array(NUMBER_OF_GAUGES, sample_length)
        intro_ids = get_introID(header_json)  # Получаем список IntroID
        for g in range(NUMBER_OF_GAUGES):
            for c in range(Event.NUMBER_OF_COMPONENTS):
                signal_data[g, c].timeDetected = intro_ids[g]  # Устанавливаем timeDetected для каждого элемента signal_data
        for ch in range(NUMBER_OF_CHANNELS):
            for i in range(sample_length):
                value = struct.unpack_from('h', data, offset)[0]
                g, c = divmod(ch, 3)
                signal_data[g, c].timeSeries[i] = value
                offset += struct.calcsize('h')

        event = Event()
        event.signalData = signal_data
        event.header = header_json
        event.catInfo = get_cat_info(seis_rec_json)
        event.UTCDate =get_date_from_header(seis_rec_json)
        print(event.UTCDate)
        return event
    else:
        return None
# def try_read(db_data):
#     MODERN_DBID = 2718281828459045
#     orig_db_data_offset = 0
#     version_id = struct.unpack_from('q', db_data, orig_db_data_offset)[0]
#     orig_db_data_offset += struct.calcsize('q')
#
#     if version_id == MODERN_DBID:
#         zipped = db_data[orig_db_data_offset:]
#         data = unzip_mem(zipped)
#         offset = 0
#
#         header_json, offset = string_from_bytes_a(data, offset)
#         hm = json.loads(header_json)
#
#         date_str = hm.get('date', '')
#         time_str = hm.get('time', '')
#
#         if date_str and time_str:
#             date_parts = date_str.split('.')
#             time_parts = time_str.split(':')
#
#             if len(date_parts) == 3 and len(time_parts) == 3:
#                 day, month, year = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
#                 hour, minute, second = map(int, time_parts)
#                 # Преобразуем дату и время в формат UTCDateTime
#                 utc_time = UTCDateTime(year, month, day, hour, minute, second)
#                 # Создаем объект Event и заполняем поле UTCDate
#                 event = Event()
#                 event.UTCDate = utc_time
#
#                 # Продолжаем обработку остальных данных...
#                 # (ваш существующий код)
#
#                 return event
#             else:
#                 print("Error: Invalid date or time format in header_json.")
#                 return None
#         else:
#             print("Error: Date or time not found in header_json.")
#             return None
#
#     else:
#         return None