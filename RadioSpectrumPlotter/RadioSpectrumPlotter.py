import xlrd  # Reading an excel file
import matplotlib.pyplot as plt  # Plotting
from prettytable import PrettyTable  # printing data


def extract_data():
    # xlsx_location = ("data/example_data.xlsx")
    xlsx_location = ("data/RF-profiling_Bronnoy_01062019.xlsx")

    workbook = xlrd.open_workbook(xlsx_location)
    sheets = [workbook.sheet_by_index(0), workbook.sheet_by_index(1)]

    x_data = [] # range(0, sheets[0].nrows - 1)*5
    for i in range(1, sheets[0].nrows):
        x_data.append(sheets[0].cell_value(i, 0))
    y_data = []
    label_names = []
    connecting_prop = []
    for i in range(len(sheets)):
        sheets[i].cell_value(0, 0)
        label_names.append(sheets[i].cell_value(0, 0))
        y_buffer = []
        connecting_prop_buf = []
        for j in range(1, sheets[i].nrows):
            y_nested_buffer = []
            for k in range(1, 4):
                value = round(sheets[i].cell_value(j, k), 4)
                y_nested_buffer.append(value)
            y_buffer.append(y_nested_buffer)
            connecting_prop_buf.append(sheets[i].cell_value(j, 4))
        connecting_prop.append(connecting_prop_buf)
        y_data.append(y_buffer)
    return x_data, y_data, connecting_prop, label_names


def calculate_average(y_data):
    y_avg = []
    for i in range(len(y_data)):
        avg_buf = []
        for j in range(len(y_data[i])):
            avg = round(sum(y_data[i][j]) / len(y_data[i][j]), 3)
            avg_buf.append(avg)
        y_avg.append(avg_buf)
    return y_avg


def print_data(x, y, avg, pr):
    table = PrettyTable()
    table.field_names = ["x_data", "y_data_0", "y_data_0_avg", "connection_pr_0",
                         "y_data_1", "y_data_1_avg", "connection_pr_1"]

    for i in range(len(x)):
        table.add_row([str(x[i]), str(y[0][i]), str(avg[0][i]), pr[0][i], str(y[1][i]), str(avg[1][i]), pr[1][i]])
    print table


def setup_plotter():
    plt.style.use('ggplot')
    plt.subplots_adjust(hspace=.025)


def show_plots():
    plt.title('AIR-ANT 2588P3M-N directional antenna')
    plt.xticks(range(0, int(x_signal_data[-1]), 10))
    plt.show()


def plot_signal_strength(x_axis, y_axis, y_avg, label_names):

    ax1 = plt.subplot(1, 1, 1)
    for i in range(len(y_axis)):
            ax1.plot(x_axis, y_axis[i], colors[0][i])
            ax1.plot(x_axis, y_avg[i], colors[1][i], label=label_names[i])

    ax1.set_ylabel("Signal strength (dBm)")
    ax1.set_xlabel('Distance (meter)')
    plt.legend()


def plot_connection_pr(x_axis, y_avg, pr, label_names):
    ax1 = plt.subplot(2, 1, 2)
    for i in range(len(y_avg)):
        ax1.plot(x_axis, pr[i], marker='.', color=colors[1][i], label=label_names[i], drawstyle='steps-pre')

    ax1.set_ylabel("Connection probability")
    ax1.set_xlabel('Distance (meter)')
    plt.legend()


# Parse data from Excel
x_signal_data, y_signal_data, connection_pr, labels = extract_data()
y_signal_avg = calculate_average(y_signal_data)
print_data(x_signal_data, y_signal_data, y_signal_avg, connection_pr)

# Plot data
colors = [['lightblue', 'lightgreen'], ['blue', 'green']]
setup_plotter()
plot_signal_strength(x_signal_data, y_signal_data, y_signal_avg, labels)
#plot_connection_pr(x_signal_data, y_signal_avg, connection_pr, labels)
show_plots()
