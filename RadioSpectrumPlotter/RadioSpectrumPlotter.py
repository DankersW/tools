import xlrd  # Reading an excel file
import matplotlib.pyplot as plt  # Plotting


def extract_data():
    xlsx_location = ("data/example_drive_away_from_ap.xlsx")

    workbook = xlrd.open_workbook(xlsx_location)
    sheets = [workbook.sheet_by_index(0), workbook.sheet_by_index(1)]

    x_data = range(0, sheets[0].nrows - 1)
    y_data = []
    label_names = []
    for i in range(len(sheets)):
        sheets[i].cell_value(0, 0)
        label_names.append(sheets[i].cell_value(0, 0))
        y_buffer = []
        for j in range(1, sheets[i].nrows):
            y_nested_buffer = []
            for k in range(1, 4):
                value = round(sheets[i].cell_value(j, k), 4)
                y_nested_buffer.append(value)
            y_buffer.append(y_nested_buffer)
        y_data.append(y_buffer)
    return x_data, y_data, label_names


def calculate_average(y_data):
    y_avg = []
    for i in range(len(y_data)):
        avg_buf = []
        for j in range(len(y_data[i])):
            avg = round(sum(y_data[i][j]) / len(y_data[i][j]), 3)
            avg_buf.append(avg)
        y_avg.append(avg_buf)
    return y_avg


def print_data(x, y, avg):
    for i in range(len(x)):
        data_message_x0 = "x_data: " + str(x[i])
        data_message_y0 = "\t y_data0: " + str(y[0][i]) + "\t y_data0_avg: " + str(avg[0][i])
        data_message_y1 = "\t y_data1: " + str(y[1][i]) + "\t y_data1_avg: " + str(avg[1][i])
        data_message = data_message_x0 + data_message_y0 + data_message_y1
        print data_message


def plot(x_axis, y_axis, y_avg, label_names):
    colors = [['lightblue', 'lightgreen'], ['blue', 'green']]
    plt.style.use('ggplot')

    ax1 = plt.subplot(1, 1, 1)
    for i in range(len(y_axis)):
            ax1.plot(x_axis, y_axis[i], colors[0][i])
            ax1.plot(x_axis, y_avg[i], colors[1][i], label=label_names[i])

    ax1.set_ylabel("Signal strength (dBm)")
    ax1.set_xlabel('Distance (meter)')

    plt.legend()
    plt.show()


x_signal_data, y_signal_data, labels = extract_data()
y_signal_avg = calculate_average(y_signal_data)
print_data(x_signal_data, y_signal_data, y_signal_avg)
plot(x_signal_data, y_signal_data, y_signal_avg, labels)
