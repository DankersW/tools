import time

from OpenLogFiles import OpenLogFiles
from DataFormatter import DataFormatter
from DataAnalyser import DataAnalyser
from DataVisualize import Datavisualization


class LogAnalyser:
    __raw_file_content = None
    __file_names = None
    __file_content = None
    __analysed_content = None

    def __init__(self):
        start_time = time.time()
        log_files = OpenLogFiles("")
        #log_files = OpenLogFiles(["logFiles/Bronnoy_WPA-80_2019-03-03_15-51-31.txt",
        #                           "logFiles/Bronnoy_NO_BGSCAN_2019-03-03_14-30-07.txt"])
        self.__raw_file_content = log_files.get_content()
        self.__file_names = log_files.get_file_names()
        print("\nEXECUTION TIME: LOG FILES OPENING --- " + str(time.time() - start_time) + " seconds ---")

        start_time = time.time()
        data_formatter = DataFormatter(self.__raw_file_content, self.__file_names)
        self.__file_content = data_formatter.get_content()
        self.__file_names = data_formatter.get_file_names()
        print("\nEXECUTION TIME: DATA FORMATTING --- " + str(time.time() - start_time) + " seconds ---")

        start_time = time.time()
        data_analyser = DataAnalyser(self.__file_content)
        self.__analysed_content = data_analyser.get_analysed_data()
        print("\nEXECUTION TIME: DATA ANALYSER --- " + str(time.time() - start_time) + " seconds ---")

        start_time = time.time()
        data_visualisation = Datavisualization(self.__analysed_content, self.__file_names)
        print("\nEXECUTION TIME: DATA VISUALISATION --- " + str(time.time() - start_time) + " seconds ---")

    def __del__(self):
        pass


if __name__ == '__main__':
    log_analyser = LogAnalyser()