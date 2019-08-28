from random import shuffle
import xlsxwriter


class FikaList:
    names = []
    start_week_number = None
    week_numbers = None

    def __init__(self, start_week_number):
        self.start_week_number = start_week_number
        with open('names.txt', 'r') as f:
            for line in f:
                self.names.append(line.strip())
        f.close()
        shuffle(self.names)
        self.week_numbers = range(start_week_number, (len(self.names) + start_week_number), 1)

    def create_excel(self):
        workbook = xlsxwriter.Workbook('fike_list.xlsx')
        worksheet = workbook.add_worksheet()
        workbook.formats[0].set_font_size(28)

        data = list()
        for i in range(len(self.names)):
            data.append([self.week_numbers[i], self.names[i]])

        table_size = 'A1:B' + str((len(data)+1))
        worksheet.add_table(table_size, {'columns': [{'header': 'Week'},
                                                     {'header': 'Name'}]})

        week_number_column_format = workbook.add_format({'align': 'center',
                                                         'font_size': 28})
        name_column_format = workbook.add_format({'font_size': 28})
        for i in range(len(self.names)):
            worksheet.write(i+1, 0, self.week_numbers[i], week_number_column_format)
            worksheet.write(i+1, 1, self.names[i], name_column_format)

        # Set column size
        worksheet.set_column(0, 0, 8)
        worksheet.set_column(1, 1, 25)

        workbook.close()


if __name__ == '__main__':
    fika_list = FikaList(36)
    fika_list.create_excel()