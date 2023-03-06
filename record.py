class Record:

    def __init__(self) -> None:
        pass

    def get(self):
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    def set(self, record, score):
        rec = max(int(record), score)
        with open('record', 'w') as f:
            f.write(str(rec))