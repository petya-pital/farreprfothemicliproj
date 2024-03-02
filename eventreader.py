import json
import zipfile
import io
import struct
import numpy as np


class Event:
    NUMBER_OF_COMPONENTS = 3

    def __init__(self):
        self.header = ""
        self.catInfo = CatalogInfo()
        self.signalData = None  # Заменяем self.signalData.timeSeries на self.signalData

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
        print(header_json)
        print('sss \n')
        db_rec_json, offset = string_from_bytes_a(data, offset)
        #print( db_rec_json)
        seis_rec_json = ""
        if data[offset] == 1:  # if event is processed
            offset += 1
            seis_rec_json, offset = string_from_bytes_a(data, offset)
            print(seis_rec_json)
            print('sss \n')
        NUMBER_OF_GAUGES = get_number_of_gauges(header_json)
        NUMBER_OF_CHANNELS = NUMBER_OF_GAUGES * Event.NUMBER_OF_COMPONENTS
        sample_length = (len(data) - offset) // (struct.calcsize('h') * NUMBER_OF_CHANNELS)
        signal_data = init_signal_data_array(NUMBER_OF_GAUGES, sample_length)

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
        return event
    else:
        return None
