import tkinter as tk
from tkinter import scrolledtext
import sys
import threading

from semantic_analyzer import code

string = ""


class StdRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, string)
        self.widget.configure(state="disabled")
        self.widget.see(tk.END)

    def flush(self):
        pass  # Not needed for Tkinter text widget


class CustomInput:
    def __init__(self, parent):
        self.parent = parent
        self.input_value = ""
        self.input_ready = threading.Event()

    def prompt(self, prompt_text=""):
        self.parent.output_text.configure(state="normal")
        self.parent.output_text.insert(tk.END, prompt_text)
        self.parent.output_text.see(tk.END)
        self.parent.output_text.configure(state="disabled")
        self.parent.input_text.set("")
        self.parent.input_entry.pack()
        self.parent.input_button.pack()
        self.input_ready.clear()

    def get_input(self, prompt_text=""):
        self.prompt(prompt_text)
        self.input_ready.wait()  # Wait until input is submitted
        self.parent.input_entry.pack_forget()
        self.parent.input_button.pack_forget()
        self.parent.output_text.configure(state="normal")
        self.parent.output_text.insert(
            tk.END, self.input_value + "\n"
        )  # Display the entered input
        self.parent.output_text.see(tk.END)
        self.parent.output_text.configure(state="disabled")
        return self.input_value

    def submit_input(self):
        self.input_value = self.parent.input_text.get()
        self.input_ready.set()  # Signal that input is ready


class OutputWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Output Window")
        self.geometry("800x600")

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.output_text.pack(expand=True, fill=tk.BOTH)

        self.input_text = tk.StringVar()
        self.input_entry = tk.Entry(self, textvariable=self.input_text)
        self.input_button = tk.Button(self, text="Submit", command=self.submit_input)

        self.custom_input = CustomInput(self)

    def submit_input(self):
        self.custom_input.submit_input()


def generate(self, input_lines, output_instance):
    output_window = OutputWindow(self)

    output_window.output_text.delete("1.0", tk.END)

    # Redirect stdout and stdin
    sys.stdout = StdRedirector(output_window.output_text)
    sys.stdin = output_window.custom_input

    def run_code():
        try:
            exec("\n".join(code), {"input": output_window.custom_input.get_input})
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Restore stdout and stdin
            sys.stdout = sys.__stdout__
            sys.stdin = sys.__stdin__

    # Run the code in a separate thread to avoid blocking the main thread
    threading.Thread(target=run_code).start()
