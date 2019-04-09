from random import shuffle
from prettytable import PrettyTable


class MeetingBingo:
    buzz_words = []

    def __init__(self):
        with open('buzz_words.txt', 'r') as f:
            for line in f:
                self.buzz_words.append(line.strip())
        f.close()
        shuffle(self.buzz_words)

    def __call__(self, *args, **kwargs):
        print self.buzz_words
        t = PrettyTable(['Name', 'Age'])
        t.add_row(['Alice', 24])
        t.add_row(['Bob', 19])
        print t



if __name__ == '__main__':
    meeting_bingo = MeetingBingo()
    meeting_bingo()
