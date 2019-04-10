from random import shuffle
import xlsxwriter


class MeetingBingo:
    buzz_words = []

    MAX_ROWS = 3
    MAX_BINGO_ITEMS = 9

    title = 'Meeting room Bingo'
    description = 'To win connect 3 buzz words with a straight line.\n' \
                  'If you shout "BINGO" out loud during the meeting, Tommy Svensson buys you a pizza and a beer\n' \
                  'Good Luck!'

    def __init__(self):
        with open('buzz_words.txt', 'r') as f:
            for line in f:
                self.buzz_words.append(line.strip())
        f.close()
        shuffle(self.buzz_words)

    def __call__(self, *args, **kwargs):
        workbook = xlsxwriter.Workbook('meeting_bingo.xlsx')
        worksheet = workbook.add_worksheet()

        title_format = workbook.add_format({
            'bold': True,
            'border': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'
        })

        description_format = workbook.add_format({
            'bold': True,
            'border': True,
            'align': 'left',
            'valign': 'vcenter',
            'fg_color': 'yellow',
            'text_wrap': True
        })

        buzz_words_format = workbook.add_format({
            'bold': True,
            'border': True,
            'align': 'center',
            'valign': 'vcenter'
        })

        worksheet.set_column('A:C', 25)
        for i in range(self.MAX_ROWS+3):
            worksheet.set_row(i, 40)

        worksheet.merge_range('A1:C1', self.title, title_format)
        worksheet.merge_range('A2:C3', self.description, description_format)

        for i in range(self.MAX_BINGO_ITEMS):
            col = i / self.MAX_ROWS
            row = i - (self.MAX_ROWS * col)
            worksheet.write(col+3, row, self.buzz_words[i], buzz_words_format )

        workbook.close()


if __name__ == '__main__':
    meeting_bingo = MeetingBingo()
    meeting_bingo()
