import json


class Dataset:
    def __init__(self, path: str):
        self.file_path = path
        self.file_data = []
        self.filtered = False

    def load_csv(self):
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
                for split_line in lines[1:]:
                    split_line = split_line.strip().split(",")
                    data_vector = []
                    for i in range(len(split_line) - 1):
                        data_vector.append(float(split_line[i]))
                    data_vector.append(split_line[-1])
                    self.file_data.append(data_vector)
        except FileNotFoundError:
            print("File not found!")

    def load_txt(self):
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    self.file_data.append(line.strip())
        except FileNotFoundError:
            print("File not found!")

    def load_json(self):
        try:
            with open(self.file_path, "r") as file:
                self.file_data = json.load(file)
        except FileNotFoundError:
            print("File not found!")

    def load_data(self):
        if self.file_path.endswith('.csv'):
            self.load_csv()
        elif self.file_path.endswith('.txt'):
            self.load_txt()
        elif self.file_path.endswith('.json'):
            self.load_json()

