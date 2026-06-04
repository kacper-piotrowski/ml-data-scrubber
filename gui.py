import customtkinter
from customtkinter import filedialog
from engine import TextDataset
from utils import NoDatasetException


class ScrubberApp(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dataset = None
        self.title("ML-DataScrubber")
        self.geometry("800x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = customtkinter.CTkFrame(self)
        self.sidebar.grid(row=0, column=0, sticky="NSEW")

        self.label = customtkinter.CTkLabel(self.sidebar, text="ML-DataScrubber", font=("Arial", 20))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.load_button = customtkinter.CTkButton(self.sidebar, text="Load File", font=("Arial", 20), command=self.handle_load_file)
        self.load_button.grid(row=1, column=0, padx=10, pady=10)

        self.word_stats_button = customtkinter.CTkButton(self.sidebar, text="Word Stats", font=("Arial", 20), command=self.handle_word_stats)
        self.word_stats_button.grid(row=2, column=0, padx=10, pady=10)

        self.filter_data_button = customtkinter.CTkButton(self.sidebar, text="Filter Data", font=("Arial", 20))
        self.filter_data_button.grid(row=3, column=0, padx=10, pady=10)

        self.censor_data_button = customtkinter.CTkButton(self.sidebar, text="Censor Data", font=("Arial", 20))
        self.censor_data_button.grid(row=4, column=0, padx=10, pady=10)

        self.main_screen = customtkinter.CTkFrame(self)
        self.main_screen.grid(row=0, column=1, sticky="NSEW")

        self.contents = customtkinter.CTkTextbox(self.main_screen)
        self.contents.pack(fill="both", expand=True)

    def handle_load_file(self):
        chosen_file_path = filedialog.askopenfilename()
        if chosen_file_path:
            self.contents.insert("end", chosen_file_path)
            self.dataset = TextDataset(chosen_file_path)
            self.dataset.load_data()
            self.contents.insert("end", f"\nLoaded {len(self.dataset.file_data)} samples!")

    def handle_word_stats(self):
        try:
            if self.dataset is None:
                raise NoDatasetException("No dataset loaded!")
            unique_words = self.dataset.get_unique_words("text")
            self.contents.delete("0.0", "end")
            self.contents.insert("end", f"Unique words: {len(unique_words)}\n")
            self.contents.insert("end", unique_words)
        except NoDatasetException as e:
            self.contents.delete("0.0", "end")
            self.contents.insert("end", e.error_text)
            return

    # def handle_filter_data(self):
    #     global chosen_min_length
    #     try:
    #         if self.dataset is None:
    #             raise NoDatasetException("No dataset loaded!")
    #         chosen_min_length = customtkinter.CTkInputDialog()
    #         if chosen_min_length.isdigit() and chosen_min_length > 0:





test = ScrubberApp()
test.mainloop()