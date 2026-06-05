import json
import os
import random
import re
from pathlib import Path

from utils import BadRowException, time_func, InvalidBatchNumberException, NoDatasetException


class Dataset:
    def __init__(self, my_path):
        self.file_path = my_path
        self.file_data = []
        self.filtered = False

    def load_csv(self, has_header=False):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if not lines:
                    raise NoDatasetException(f"Empty file {self.file_path}!")
                delimiter = ';' if ';' in lines[0] else ','
                if has_header:
                    headers = lines[0].strip().split(delimiter)
                else:
                    headers = ["col "+str(i) for i in range(len(lines[0].split(delimiter)))]
                start_index = 1 if has_header else 0
                for split_line in lines[start_index:]:
                    try:
                        split_line = split_line.strip().split(delimiter)
                        if len(split_line) != len(headers):
                            raise BadRowException(start_index, "CSV row has wrong number of columns")
                        data_dict = dict(zip(headers, split_line))
                        self.file_data.append(data_dict)
                        start_index += 1
                    except BadRowException as e:
                        print(e.error_text)
                        continue
        except FileNotFoundError:
            raise NoDatasetException(f"Can't find the file {self.file_path}!")
        except Exception as e:
            raise NoDatasetException(f"Error loading CSV file: {str(e)}")

    def load_txt(self):
        header = "text"
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():
                        data_dict = {header: line.strip()}
                        self.file_data.append(data_dict)
        except FileNotFoundError:
            raise NoDatasetException(f"Can't find the file {self.file_path}!")

    def load_json(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.file_data = json.load(file)
        except FileNotFoundError:
            print("File not found!")

    @time_func
    def load_data(self, has_header=False):
        if self.file_path.endswith('.csv'):
            self.load_csv(has_header=has_header)
        elif self.file_path.endswith('.txt'):
            self.load_txt()
        elif self.file_path.endswith('.json'):
            self.load_json()

    def generate_batches(self, batch_size):
        for i in range(0, len(self.file_data), batch_size):
            yield self.file_data[i:i + batch_size]

    @time_func
    def export_batches(self, batch_size, format_type="json"):
        if batch_size > len(self.file_data):
            raise InvalidBatchNumberException(f"Can't generate {batch_size} from {len(self.file_data)} rows of data!")
        os.makedirs("batches", exist_ok=True)
        base_name = "batches"
        if self.file_path:
            base_name = Path(self.file_path).stem
        batch_size = max(1, batch_size)
        random.shuffle(self.file_data)
        batches = self.generate_batches(batch_size)
        for number, batch in enumerate(batches):
            generated_batch_name = f"{base_name}_{number}.{format_type}"
            with open("batches/" + generated_batch_name, "w", encoding="utf-8") as file:
                if format_type == "json":
                    json.dump(batch, file, indent=4)

    def get_columns(self):
        if self.file_data and isinstance(self.file_data[0], dict):
            return list(self.file_data[0].keys())
        return []

class TextDataset(Dataset):
    def __init__(self, my_path: str):
        super().__init__(my_path)

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
        filtered_data = list(filter(lambda current_dict: len(current_dict[column].split()) >= min_length, self.file_data))
        self.file_data = filtered_data

    def censor_personal_data(self, column, personal_data_type):
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

