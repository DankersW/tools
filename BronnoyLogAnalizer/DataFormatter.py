class DataFormatter:
    __raw_content = None
    __file_names = None
    __content = None

    def __init__(self, raw_content, file_names):
        self.__raw_content = raw_content
        self.__file_names = file_names
        self.parse_raw_content(raw_content, file_names)

    def __del__(self):
        pass

    def parse_raw_content(self, raw_content, files):
        """
        Parse each value from the nested list from string to float data type and check if the data is correct to
        continue.
        checks:
            -The vehicle communicated during the test. Important since we want to check the communication.
            -Each data row contains exactly 8 arguments.
            -Check if the vehicle moved during the test. Important since we want the know the signal strength at different
                position at the track.

        :param raw_content: The unparsed raw content from each log file in [logFile][row][value] format as string datatype.
        :param files: all the file names that needs to be parsed.
        :return: a parsed float nested list [logFile][row][value] of the usable data from the logfiles, and an updated
            version of the file names currently in use
        """
        print ("\nStarting to parse the data...")

        content = []
        to_pop_list = []
        for i in range(len(raw_content)):
            log_buf = []
            conversion_error = False
            for j in range(len(raw_content[i])):
                try:
                    buf = [float(x) for x in raw_content[i][j].split(",")]
                    log_buf.append(buf)
                except (ValueError, IndexError):
                    conversion_error = True

            if conversion_error:
                print (files[i] + ": \t FAILED: conversion error detected")
                to_pop_list.append(i)
            elif len(log_buf) == 0:  # vehicle didn't communicate
                print (files[i] + ": Vehicle did not communicated! The log will be remove from the analysis")
                to_pop_list.append(i)
            elif log_buf[-1][2] - log_buf[0][2] < 5:  # vehicle didn't drive
                print (files[i] + ": Vehicle did not move! The log will be remove from the analysis")
                to_pop_list.append(i)
            else:
                print (files[i] + ": Successfully parsed the data")
                content.append(log_buf)

        for i in reversed(to_pop_list):
            files.pop(i)

        self.__content = content
        self.__file_names = files

    def get_file_names(self):
        return self.__file_names

    def get_content(self):
        return self.__content


if __name__ == '__main__':
    formatter = DataFormatter()
