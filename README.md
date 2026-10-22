# ML-DataScrubber
The goal of this project is to enable easy operations on files later used for training Machine Learning models. It is a GUI application that supports cleaning, analyzing, and preparing data in CSV, TXT, and JSON formats.

## Main Features:
- **Data loading:** supports CSV files with or without headers
- **Word statistics:** displays the total count and list of unique words, and generates a bar chart of the 10 most frequent words
- **Data filtering:** removes rows shorter than a user-specified length threshold
- **Data censoring (anonymization):** predefined regular expressions for email addresses, PESEL numbers, and Polish phone numbers that mask sensitive data
- **Training file splitting:** randomly shuffles data and exports batches of a user-defined size using a generator

## Libraries Used:
- **Python Standard Library:** `json`, `csv`, `re`, `random`, `pathlib`, `time`, `functools`
- **External Libraries:**
  - `customtkinter` - used for building the graphical user interface
  - `matplotlib` - used for dynamically plotting word frequency charts

## Project Structure:
- `main.py` - starts the main GUI loop
- `gui.py` - user interface definition, logical event handling, and user interactions
- `engine.py` - core logic for all program features and definitions of the `Dataset` and `TextDataset` classes
- `utils.py` - contains all custom exceptions and a decorator for logging function execution time

## How to Run:
1. Extract the project archive
2. Install required libraries:
```bash
pip install customtkinter matplotlib
 ```
3. Run the application:
```bash
python main.py
```

## Custom Exceptions:
- BadRowException - raised when a row in a CSV file has an invalid number of columns
- NoDatasetException - raised when no data is loaded to perform a requested operation
- InvalidBatchNumberException - raised when the specified batch size exceeds the total number of rows
