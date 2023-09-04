import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from deep_translator import GoogleTranslator
from ttkthemes import ThemedStyle

LANGUAGES = {
    "en": "English",
    "vi": "Vietnamese",
    "fr": "French",
    "es": "Spanish",
    # Add more languages here...
}

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Egy Translator")
        self.style = ThemedStyle(self.root)
        self.style.set_theme("equilux")  # Choose a different theme

        self.style.configure('.', font=('Helvetica', 14))
        self.style.configure('TButton', font=('Helvetica', 14))

        banner_frame = ttk.Frame(root)
        banner_frame.pack(fill="x", padx=20, pady=20)
        ttk.Label(banner_frame, text="Egy Translator", font=("Helvetica", 24)).pack()

        frame = ttk.Frame(root)
        frame.pack(padx=20, pady=(0, 20))

        source_label = ttk.Label(frame, text="Source Language:")
        source_label.grid(row=0, column=0, padx=(0, 10))

        self.source_language = ttk.Combobox(frame, values=list(LANGUAGES.values()), state="readonly", width=20)
        self.source_language.set("English")
        self.source_language.grid(row=0, column=1)

        target_label = ttk.Label(frame, text="Target Language:")
        target_label.grid(row=0, column=2, padx=(10, 0))

        self.target_language = ttk.Combobox(frame, values=list(LANGUAGES.values()), state="readonly", width=20)
        self.target_language.set("Vietnamese")
        self.target_language.grid(row=0, column=3)

        self.translate_button = ttk.Button(frame, text="Translate", command=self.translate, style="TButton")
        self.translate_button.grid(row=0, column=4, padx=(10, 0))

        self.select_file_button = ttk.Button(frame, text="Select File", command=self.load_file, style="TButton")
        self.select_file_button.grid(row=0, column=5)

        # Initialize the source_text
        self.source_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=50, bg='white', fg='black')
        self.source_text.pack(padx=20, pady=(0, 20))

        self.result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=50, state="disabled", bg='light gray')
        self.result_text.pack(padx=20, pady=(0, 20))

        self.root.bind('<Return>', lambda event=None: self.translate())

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            # Ensure that the file path is safe
            if file_path.startswith(("C:/", "/home/")):  # Adjust as needed for your environment
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.source_text.delete("1.0", "end")
                    self.source_text.insert("1.0", "file://" + file_path)
            else:
                self.show_error("Invalid file path")

    def translate(self):
        source_language_name = self.source_language.get()
        target_language_name = self.target_language.get()

        if source_language_name == target_language_name:
            self.show_error("Source and target languages are the same.")
            return

        source_language_code = [code for code, name in LANGUAGES.items() if name == source_language_name][0]
        target_language_code = [code for code, name in LANGUAGES.items() if name == target_language_name][0]

        source_text = self.source_text.get("1.0", "end-1c")

        if source_text:
            try:
                if source_text.startswith("file://"):
                    # Translate content of the selected file
                    file_path = source_text[len("file://"):]
                    # Ensure that the file path is safe
                    if file_path.startswith(("C:/", "/home/")):  # Adjust as needed for your environment
                        with open(file_path, 'r', encoding='utf-8') as file:
                            source_text = file.read()
                    else:
                        self.show_error("Invalid file path")

                # Translate the text
                translation = GoogleTranslator(source=source_language_code, target=target_language_code).translate(source_text)

                self.result_text.config(state="normal")
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", translation)
                self.result_text.config(state="disabled")

                # Save the translated content to a new file
                translated_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
                if translated_file_path:
                    # Ensure that the file path is safe
                    if translated_file_path.startswith(("C:/", "/home/")):  # Adjust as needed for your environment
                        with open(translated_file_path, 'w', encoding='utf-8') as translated_file:
                            translated_file.write(translation)
                    else:
                        self.show_error("Invalid file path")
            except Exception as e:
                self.show_error(f"Translation Error: {str(e)}")
        else:
            self.show_error("Source text is empty")

    def show_error(self, message):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", f"Error: {message}")
        self.result_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
