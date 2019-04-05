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

        bold = workbook.add_format({'bold': True})
        worksheet.write(0, 0, 'Week', bold)
        worksheet.write(0, 1, 'Name', bold)

        for i in range(len(self.names)):
            worksheet.write(i+1, 0, self.week_numbers[i])
            worksheet.write(i+1, 1, self.names[i])

        workbook.close()


if __name__ == '__main__':
    fikaList = FikaList(15)
    fikaList.create_excel()


