import tkinter as tk
from lexical_analyzer import is_lexical_valid

# REF(TextLineNumbers, CustomText): https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget


class _TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)


class _CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (
            args[0] in ("insert", "replace", "delete")
            or args[0:3] == ("mark", "set", "insert")
            or args[0:2] == ("xview", "moveto")
            or args[0:2] == ("xview", "scroll")
            or args[0:2] == ("yview", "moveto")
            or args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result


class CodeEditorFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = _CustomText(self, wrap="none")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.linenumbers = _TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

    def _on_change(self, event):
        self.linenumbers.redraw()

    def get_text(self):
        return self.text.get("1.0", "end-1c").splitlines(True)


class _HeadersFrame(tk.Frame):

    def __init__(
        self,
        *args,
        output_instance=None,
        token_instance=None,
        code_editor_instance=None,
        **kwargs,
    ):
        tk.Frame.__init__(self, *args, **kwargs)
        self.output_instance = output_instance
        self.token_instance = token_instance
        self.code_editor_instance = code_editor_instance

        self.lexBtn = tk.Button(
            self,
            text="Analyze",
            font=("Arial", 12, "bold"),
            activebackground="lightblue",
            command=self._analyze,
        )
        self.lexBtn.pack(side="left", padx=5, pady=5)

        self.stageLbl = tk.Label(
            self, text="Compiler Stage: ", font=("Arial", 12, "bold")
        )
        self.stageLbl.pack(side="left", padx=100, pady=5)

    def _analyze(self):
        """Analyze the input code"""
        self.output_instance.clear_output()
        self.token_instance.clear_tokens()

        self.stageLbl.configure(text="Compiler Stage: Lexical Analysis")
        if is_lexical_valid(
            self.output_instance,
            self.token_instance,
            self.code_editor_instance.get_text(),
        ):
            pass


class OutputFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.outputLabel = tk.Label(self, text="Ouput", font=("Arial", 14, "bold"))
        self.outputLabel.pack(anchor="w")

        self.outputText = tk.Text(
            self,
            font=("Arial", 12),
            bd=2,
            relief="solid",
            state="disabled",
            height=15,
        )
        self.outputText.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def set_output(self, output: str):
        """Set the output text in the Output Frame"""
        self.outputText.configure(state="normal")
        self.outputText.insert(tk.END, output)
        self.outputText.configure(state="disabled")

    def clear_output(self):
        """Clear the output text in the Output Frame"""
        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", tk.END)
        self.outputText.configure(state="disabled")


class TokenTableFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.lexicLbl = tk.Label(
            self, text="Token : Lexeme", font=("Arial", 14, "bold")
        )
        self.lexicLbl.pack(anchor="w")

        self.tokenText = tk.Text(
            self,
            font=("Arial", 12),
            bd=2,
            relief="solid",
            state="disabled",
            width=25,
            wrap="none",
        )
        self.tokenText.pack(fill=tk.Y, expand=True, padx=5, pady=5)

    def set_tokens(self, output):
        """Set the token text in the Token Frame"""
        self.tokenText.configure(state="normal")

        for token in output:
            if token[1] == "<newline>":
                continue
            self.tokenText.insert(tk.END, f"{token[0]}\t\t:    {token[1]}\n")

        self.tokenText.configure(state="disabled")

    def clear_tokens(self):
        """Clear the token text in the Token Frame"""
        self.tokenText.configure(state="normal")
        self.tokenText.delete("1.0", tk.END)
        self.tokenText.configure(state="disabled")


class _MainFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.token = TokenTableFrame(self)
        self.output = OutputFrame(self)
        self.codeEditor = CodeEditorFrame(self)
        self.headers = _HeadersFrame(
            self,
            output_instance=self.output,
            token_instance=self.token,
            code_editor_instance=self.codeEditor,
        )

        # Grid layout
        self.headers.grid(row=0, column=0, sticky="nsew", padx=30)
        self.codeEditor.grid(row=1, column=0, sticky="nsew")
        self.output.grid(row=2, column=0, sticky="nsew", pady=10)
        self.token.grid(row=0, column=1, rowspan=3, sticky="nsew", pady=10)

        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


if __name__ == "__main__":
    # Create the main window
    window = tk.Tk()
    window.title("Compiler")
    window.minsize(800, 600)

    # Create the main app
    main = _MainFrame(window)

    # layout
    main.pack(side="left", fill="both", expand=True)

    window.mainloop()
