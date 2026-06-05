import customtkinter
import matplotlib.pyplot as plot
from customtkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from engine import TextDataset
from utils import NoDatasetException, InvalidBatchNumberException


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

        self.filter_data_button = customtkinter.CTkButton(self.sidebar, text="Filter Data", font=("Arial", 20), command=self.handle_filter_data)
        self.filter_data_button.grid(row=3, column=0, padx=10, pady=10)

        self.censor_data_button = customtkinter.CTkButton(self.sidebar, text="Censor Data", font=("Arial", 20), command=self.handle_censor_data)
        self.censor_data_button.grid(row=4, column=0, padx=10, pady=(10,0))
        self.censor_options = customtkinter.CTkOptionMenu(self.sidebar, values=["email", "pl_phone", "pesel"])
        self.censor_options.grid(row=5, column=0, padx=10, pady=(0,10))

        self.filter_data_button = customtkinter.CTkButton(self.sidebar, text="Export Batches", font=("Arial", 20), command=self.handle_export_batches)
        self.filter_data_button.grid(row=6, column=0, padx=10, pady=10)

        self.main_screen = customtkinter.CTkFrame(self)
        self.main_screen.grid(row=0, column=1, sticky="NSEW")

        self.contents = customtkinter.CTkTextbox(self.main_screen)
        self.contents.pack(fill="both", expand=True)
        self.contents.configure(state="disabled")

    def update_console(self, text, clear_before = False):
        self.contents.configure(state="normal")
        if clear_before:
            self.contents.delete("0.0", "end")
        self.contents.insert("end", text)
        self.contents.configure(state="disabled")

    def handle_load_file(self):
        chosen_file_path = filedialog.askopenfilename()
        if chosen_file_path:
            self.update_console(chosen_file_path)
            self.dataset = TextDataset(chosen_file_path)
            self.dataset.load_data()
            self.update_console(f"\nLoaded {len(self.dataset.file_data)} lines!")

    def handle_word_stats(self):
        try:
            if self.dataset is None:
                raise NoDatasetException("No dataset loaded!")
            frequency_dict = self.dataset.get_word_frequencies("text") #TODO KOLUMNA!!
            top_10 = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)[:10]
            words = [pair[0] for pair in top_10]
            counts = [pair[1] for pair in top_10]
            plot.style.use("dark_background")
            plot_window = customtkinter.CTkToplevel(self)
            plot_window.title("Word Stats")
            plot_window.geometry("800x600")
            plot_window.attributes("-topmost", True)
            figure = plot.figure(figsize = (8,5))
            figure.patch.set_facecolor("#1d1e1e")
            axes = plot.gca()
            axes.set_facecolor("#1d1e1e")
            plot.bar(words, counts, color="#1f6aa5")
            plot.title("Top 10 Most Frequent Words")
            plot.xlabel("Words")
            plot.ylabel("Frequency")
            plot.xticks(rotation=45)
            plot.tight_layout()

            def save_plot():
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
                    title="Save chart as...",
                )
                if file_path:
                    figure.savefig(file_path)
            save_plot_button = customtkinter.CTkButton(plot_window, text="Save File", command=save_plot)
            save_plot_button.pack(pady=10, side="bottom")

            canvas = FigureCanvasTkAgg(figure, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            unique_words = self.dataset.get_unique_words("text")  # TODO KOLUMNA!!
            self.update_console(f"Unique words: {len(unique_words)}\n\n", clear_before=True)
            for word in unique_words:
                self.update_console(f"{word}\n")
        except NoDatasetException as e:
            self.update_console(e.error_text, clear_before=True)
            return

    def handle_filter_data(self):
        try:
            if self.dataset is None:
                raise NoDatasetException("No dataset loaded!")
            chosen_min_length_box = customtkinter.CTkInputDialog(text="Choose the minimal number of words in a row", title="Choice")
            chosen_min_length = chosen_min_length_box.get_input()
            if chosen_min_length and chosen_min_length.isdigit() and int(chosen_min_length) > 0:
                old_length = len(self.dataset.file_data)
                self.dataset.filter_short_data("text", int(chosen_min_length)) #TODO KOLUMNA!!
                new_length = len(self.dataset.file_data)
                removed_count = old_length - new_length
                self.update_console(f"Data filtered!\n", clear_before=True)
                self.update_console(f"Removed {removed_count} short rows.\n")
                self.update_console(f"Remaining rows: {new_length}\n\n")
                self.update_console("Preview: \n")
                for row in self.dataset.file_data[:5]:
                    self.update_console(f"{row}\n")
        except NoDatasetException as e:
            self.update_console(e.error_text, clear_before=True)

    def handle_censor_data(self):
        try:
            if self.dataset is None:
                raise NoDatasetException("No dataset loaded!")
            chosen_censor = self.censor_options.get()
            self.dataset.censor_personal_data("text", chosen_censor) #TODO KOLUMNA!!
            self.update_console(f"Censored {chosen_censor} in dataset!\n", clear_before=True)
        except NoDatasetException as e:
            self.update_console(e.error_text, clear_before=True)

    def handle_export_batches(self):
        try:
            if self.dataset is None:
                raise NoDatasetException("No dataset loaded!")
            chosen_batches_box = customtkinter.CTkInputDialog(text="Choose the batch size (number of rows per file)",title="Choice")
            chosen_batches = chosen_batches_box.get_input()
            if chosen_batches and chosen_batches.isdigit() and int(chosen_batches) > 0:
                self.dataset.export_batches(int(chosen_batches))
                self.update_console(f"Successfully exported {chosen_batches} rows per batch!\n", clear_before=True)
        except NoDatasetException as e:
            self.update_console(e.error_text, clear_before=True)
        except InvalidBatchNumberException as e:
            self.update_console(e.error_text, clear_before=True)

