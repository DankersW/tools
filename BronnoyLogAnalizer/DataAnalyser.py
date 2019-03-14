class DataAnalyser:
    __data = None

    ODO_NUM = 2
    RX_BROAD_NUM = 7
    RX_UNI_NUM = 8
    TIME_NUM = 0

    def __init__(self, data):
        self.__data = data
        self.calc_rx_packets_and_transmission_time_and_sync_odo()

    def __del__(self):
        pass

    def calc_rx_packets_and_transmission_time_and_sync_odo(self):
        """
        Calculate the amount of received packets (rx) for each row, calculate the transmission time, and synchronize the
            odometer value with zero.

        rx calculation: previous_entry_packet_counter - current_entry_packet_counter = the amount of received packets for
            that entry.
        transmission time calculation: (previous_entry_transmission_time - current_entry_transmission_time) / amount_of_rx
            = the time it took on average to transmit a packet
        odometer sync: current_odo_value - start_odo_value = transversed distance in comparison with the previous entry.

        :param data: The parsed nested list containing all the data
        :return: a updated version of the data nested list
        """
        for i in range(len(self.__data)):
            self.__data[i][0].append(0)
            self.__data[i][0].append(0)
            self.__data[i][0].append(0)
            init_odo = self.__data[i][0][self.ODO_NUM]
            for j in range(1, len(self.__data[i])):
                rx_broad_buf = self.__data[i][j][self.RX_BROAD_NUM] - self.__data[i][j - 1][self.RX_BROAD_NUM]
                rx_uni_buf = self.__data[i][j][self.RX_UNI_NUM] - self.__data[i][j - 1][self.RX_UNI_NUM]

                time_buf = (self.__data[i][j][self.TIME_NUM] - self.__data[i][j - 1][self.TIME_NUM])
                if time_buf != 0 and rx_broad_buf != 0:  # Possible divide by zero instances
                    time_buf = time_buf / rx_broad_buf
                if time_buf != 0 and rx_uni_buf != 0:  # Possible divide by zero instances
                    time_buf = time_buf / rx_uni_buf

                odo_buf = self.__data[i][j][self.ODO_NUM] - init_odo

                self.__data[i][j].append(time_buf)
                self.__data[i][j].append(rx_broad_buf)
                self.__data[i][j].append(rx_uni_buf)
                self.__data[i][j][self.ODO_NUM] = odo_buf
                self.__data[i][0][9] = self.__data[i][1][9]

    def get_analysed_data(self):
        return self.__data


if __name__ == '__main__':
    data_analyser = DataAnalyser
