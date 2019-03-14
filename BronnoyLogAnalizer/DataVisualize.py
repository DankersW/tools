import matplotlib.pyplot as plt  # Plotting

class Datavisualization:
    __file_names = None
    __entrances = None
    __data = None

    __data_x_axis_odo = []
    __data_y_axis_udp_broad = []
    __data_y_axis_udp_uni = []

    def __init__(self, data, files):
        self.__data = data
        self.__file_names = files

        self.find_entrances(self.__data)
        self.plot_packet_arrival_and_speed_over_odo()

    def __del__(self):
        pass

    def find_entrances(self, data):
        """
        Finds the coordinates of the entrances by comparing the in tunnel variable ([5]) with the previous entry value. If
            this one has changed one knows that the vehicle pasted a tunnel entrance. The entrance number is also present
            ([5]). Used to visualize the difference between in and outside of a tunnel.
        :param data: The parsed nested list containing all the data
        :return: a nested list constraining the entrance coordinates and the entrance number
        """
        entrances = []
        for i in range(len(data)):
            entrance_buf = []
            for j in range(1, len(data[i])):
                if data[i][j - 1][5] != data[i][j][5]:
                    entrance_buf.append([int(data[i][j][5]), data[i][j][2], int(data[i][j][6])])
            entrances.append(entrance_buf)
        self.__entrances = entrances

        for i in range(250):
            print data[1][i]
        print entrances[1]


    def plot_packet_arrival_and_speed_over_odo(self):
        """
        Visualizes the amount of received packets, speed, and average packet transmission time values over odometer value
            using MatplotLib
        :param data: The parsed nested list containing all the data
        :param files: All the used log files (plot title)
        :param entrances: nested list of the tunnel entrances
        """
        for i in range(len(self.__data)):
            #plt.figure(i)

            data_x_axis_odo = []
            data_y_axis_udp_broad = []
            data_y_axis_udp_uni = []
            data_y_axis_speed = []
            data_y_axis_time = []

            # Generate data
            for j in range(1, len(self.__data[i])):
                if self.__data[i][j - 1][2] != self.__data[i][j][2]:  # Only select the moving points
                    data_x_axis_odo.append(self.__data[i][j][2])
                    data_y_axis_udp_broad.append(self.__data[i][j][10])
                    data_y_axis_udp_uni.append(self.__data[i][j][11])
                    data_y_axis_speed.append(self.__data[i][j][7])
                    data_y_axis_time.append(self.__data[i][j][9])

            self.__data_x_axis_odo.append(data_x_axis_odo)
            self.__data_y_axis_udp_broad.append(data_y_axis_udp_broad)
            self.__data_y_axis_udp_uni.append(data_y_axis_udp_uni)

            # # Create the sub plots
            # ax1 = plt.subplot(3, 1, 1)
            # ax1.plot(data_x_axis_odo, data_y_axis_udp_broad, 'gX-', label='Broadcast packets')
            # ax1.plot(data_x_axis_odo, data_y_axis_udp_uni, 'rX-', label='Unicast packets')
            # plt.title(self.__file_names[i])
            # ax1.set_ylabel('Received UDP packets')
            #
            # # Annotate the tunnel entrances
            # lim_udp = ax1.get_ylim()
            #
            # for j in range(len(self.__entrances[i])):
            #     # Entrance lines
            #     ax1.plot([self.__entrances[i][j][1], self.__entrances[i][j][1]], lim_udp, 'k-')
            #
            #     # Entrance labels + tunnel
            #     tunnel = ""
            #     if self.__entrances[i][j][2] == 1:
            #         tunnel = " IN"
            #     ax1.text(self.__entrances[i][j][1], (lim_udp[0] + (lim_udp[0] / 10)),
            #              str(self.__entrances[i][j][0]) + tunnel)

        # Create the sub plots
        ax1 = plt.subplot(5, 1, 1)
        ax1.plot(self.__data_x_axis_odo[1], self.__data_y_axis_udp_broad[1], 'gX-')
        #ax1.plot(self.__data_x_axis_odo[1], self.__data_y_axis_udp_uni[1], 'rX-')
        ax1.set_ylabel(self.__file_names[1])

        ax2 = plt.subplot(5, 1, 2)
        ax2.plot(self.__data_x_axis_odo[2], self.__data_y_axis_udp_broad[2], 'gX-')
        #ax2.plot(self.__data_x_axis_odo[2], self.__data_y_axis_udp_uni[2], 'rX-')
        ax2.set_ylabel(self.__file_names[2])

        ax3 = plt.subplot(5, 1, 3)
        ax3.plot(self.__data_x_axis_odo[3], self.__data_y_axis_udp_broad[3], 'gX-')
        #ax3.plot(self.__data_x_axis_odo[3], self.__data_y_axis_udp_uni[3], 'rX-')
        ax3.set_ylabel(self.__file_names[3])

        ax4 = plt.subplot(5, 1, 4)
        ax4.plot(self.__data_x_axis_odo[4], self.__data_y_axis_udp_broad[4], 'gX-')
        #ax4.plot(self.__data_x_axis_odo[4], self.__data_y_axis_udp_uni[4], 'rX-')
        ax4.set_ylabel(self.__file_names[4])

        ax5 = plt.subplot(5, 1, 5)
        ax5.plot(self.__data_x_axis_odo[5], self.__data_y_axis_udp_broad[5], 'gX-', label='Broadcast packets')
        #ax5.plot(self.__data_x_axis_odo[5], self.__data_y_axis_udp_uni[5], 'rX-', label='Unicast packets')
        ax5.set_ylabel(self.__file_names[5])
        ax5.set_ylim(0, 10)


        ax5.set_xlabel('Odometer')

        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()


if __name__ == '__main__':
    visu = Datavisualization()