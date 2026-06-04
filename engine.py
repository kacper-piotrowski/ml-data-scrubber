import json
import re


class Dataset:
    def __init__(self, path):
        self.file_path = path
        self.file_data = []
        self.filtered = False

    def load_csv(self, has_header=False):
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
                if has_header:
                    headers = lines[0].strip().split(',')
                else:
                    headers = ["col "+str(i) for i in range(len(lines[0].split(',')))]
                start_index = 1 if has_header else 0
                for split_line in lines[start_index:]:
                    split_line = split_line.strip().split(",")
                    data_dict = dict(zip(headers, split_line))
                    self.file_data.append(data_dict)
        except FileNotFoundError:
            print("File not found!")

    def load_txt(self):
        header = "text"
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    data_dict = {header: line.strip()}
                    self.file_data.append(data_dict)
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

class TextDataset(Dataset):
    def __init__(self, path: str):
        super().__init__(path)

    def get_unique_words(self, column):
        return {word for current_dict in self.file_data for word in current_dict[column].split()}

    def get_word_frequencies(self, column):
        frequency_dict = dict()
        for current_dict in self.file_data:
            for word in current_dict[column].split():
                if word not in frequency_dict:
                    frequency_dict[word] = 1
                else:
                    frequency_dict[word] += 1
        return frequency_dict

    def filter_short_data(self, column, min_length):
        filtered_data = list(filter(lambda current_dict: len(current_dict[column]) >= min_length, self.file_data))
        self.file_data = filtered_data

    def mask_personal_data(self, column, personal_data_type):
        personal_data_patterns = {
            "email" : r'\S+@\S+',
            "pl_phone" : r'\b\d{9}\b',
            "pesel" : r'\b\d{11}\b'
        }
        chosen_pattern = personal_data_patterns.get(personal_data_type)
        if not chosen_pattern:
            print(f"Invalid personal data type: {personal_data_type}")
            return
        for current_dict in self.file_data:
            masked_dict = re.sub(chosen_pattern, "[PERSONAL]", current_dict[column])
            current_dict[column] = masked_dict

