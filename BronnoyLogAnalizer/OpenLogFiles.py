import os   # File names


class OpenLogFiles:
    __files_names = None
    __content = None

    def __init__(self, input_file):
        if not input_file:
            self.find_log_file_names()
        else:
            self.__files_names = input_file

        self.open_log_file()

    def __del__(self):
        pass

    def find_log_file_names(self):
        """
        Find and save all the .txt files who reside in the current directory.
        :return: A list of .txt file names
        """
        files = []
        print ("No file names where provided. Selecting all files with .txt extension from the current directory.")
        os.chdir("logFiles")
        for log_file in os.listdir(os.getcwd()):
            if log_file.endswith(".txt"):
                files.append(log_file)
        self.__files_names = files

    def open_log_file(self):
        """
        Read the provided files and save the data in a list
        :exception: only append the files which are readable
        :param: file_names: all the .txt files from the current directory or the PATH/FILE specified by the user in the
        arguments.
        :returns: the content of the provided files [logFile][row][value], and an updated version of the file name list
        """
        print ("Opening the following .txt log files:")
        content = []
        error_content = []
        to_pop_list = []
        for i in range(len(self.__files_names)):
            try:
                with open(self.__files_names[i]) as f:
                    buf = f.readlines()
                buf = [x.strip() for x in buf]
                content.append(buf)
                error_content.append("")
            except IOError:
                error_content.append("\t FAILED: Could not open file.")
                to_pop_list.append(i)
            print ("\t-" + self.__files_names[i] + error_content[i])

        for i in reversed(to_pop_list):
            self.__files_names.pop(i)

        self.__content = content

    def get_content(self):
        return self.__content

    def get_file_names(self):
        return self.__files_names


if __name__ == '__main__':
    open_log_files = OpenLogFiles(["logFiles/Bronnoy_WPA-80_2019-03-03_15-51-31.txt", "logFiles/Bronnoy_NO_BGSCAN_2019-03-03_14-30-07.txt"])
    #open_log_files = OpenLogFiles("")