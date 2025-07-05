import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fpdf import FPDF
from spellchecker import SpellChecker

class ResumeSection:
    def __init__(self, title="Section", content=""):
        self.title = title
        self.content = content

class ResumeBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Resume Word Processor")

        self.sections = []
        self.selected_section = None
        self.spell = SpellChecker()

        self.create_widgets()

    def create_widgets(self):
        # Section management
        self.section_frame = tk.Frame(self.root)
        self.section_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.section_listbox = tk.Listbox(self.section_frame)
        self.section_listbox.pack(fill=tk.BOTH, expand=1)
        self.section_listbox.bind('<<ListboxSelect>>', self.on_section_select)

        btn_add = tk.Button(self.section_frame, text="Add Section", command=self.add_section)
        btn_remove = tk.Button(self.section_frame, text="Remove Section", command=self.remove_section)
        btn_add.pack(fill=tk.X)
        btn_remove.pack(fill=tk.X)

        # Editor
        editor_frame = tk.Frame(self.root)
        editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

        # Formatting toolbar
        toolbar = tk.Frame(editor_frame)
        toolbar.pack(fill=tk.X)
        tk.Button(toolbar, text="Bold", command=self.make_bold).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Italic", command=self.make_italic).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Underline", command=self.make_underline).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Spell Check", command=self.spell_check).pack(side=tk.LEFT)

        tk.Label(toolbar, text="Font Size:").pack(side=tk.LEFT, padx=5)
        self.font_size_var = tk.IntVar(value=12)
        font_size_menu = ttk.Combobox(toolbar, textvariable=self.font_size_var, values=list(range(8, 25)), width=3)
        font_size_menu.pack(side=tk.LEFT)
        font_size_menu.bind("<<ComboboxSelected>>", self.set_font_size)

        # Text area
        self.text = tk.Text(editor_frame, wrap='word', font=('Arial', 12))
        self.text.pack(fill=tk.BOTH, expand=1)

        # Save/Export
        btn_frame = tk.Frame(editor_frame)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Save Section", command=self.save_section_content).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Export to PDF", command=self.export_to_pdf).pack(side=tk.LEFT)

    # Section Management
    def add_section(self):
        title = tk.simpledialog.askstring("Section Title", "Enter section title:")
        if title:
            sec = ResumeSection(title=title)
            self.sections.append(sec)
            self.section_listbox.insert(tk.END, title)

    def remove_section(self):
        idx = self.section_listbox.curselection()
        if not idx:
            return
        del self.sections[idx[0]]
        self.section_listbox.delete(idx[0])
        self.text.delete(1.0, tk.END)

    def on_section_select(self, event):
        idx = self.section_listbox.curselection()
        if not idx:
            return
        self.selected_section = idx[0]
        section = self.sections[self.selected_section]
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, section.content)

    def save_section_content(self):
        if self.selected_section is not None:
            self.sections[self.selected_section].content = self.text.get(1.0, tk.END).strip()
            messagebox.showinfo("Saved", "Section content saved.")

    # Formatting
    def make_bold(self):
        self._tag_selected("bold", ("Arial", self.font_size_var.get(), "bold"))

    def make_italic(self):
        self._tag_selected("italic", ("Arial", self.font_size_var.get(), "italic"))

    def make_underline(self):
        self._tag_selected("underline", ("Arial", self.font_size_var.get(), "underline"))

    def _tag_selected(self, tag, font):
        try:
            start = self.text.index(tk.SEL_FIRST)
            end = self.text.index(tk.SEL_LAST)
            self.text.tag_add(tag, start, end)
            self.text.tag_configure(tag, font=font)
        except tk.TclError:
            pass

    def set_font_size(self, event=None):
        size = self.font_size_var.get()
        self.text.config(font=('Arial', size))

    # Spell check
    def spell_check(self):
        content = self.text.get(1.0, tk.END)
        words = content.split()
        misspelled = self.spell.unknown(words)
        if misspelled:
            messagebox.showinfo("Spell Check", f"Misspelled words: {', '.join(misspelled)}")
        else:
            messagebox.showinfo("Spell Check", "No spelling mistakes found.")

    # Export to PDF
    def export_to_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not file_path:
            return
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for section in self.sections:
            pdf.set_font("Arial", style='B', size=14)
            pdf.cell(0, 10, section.title, ln=1)
            pdf.set_font("Arial", size=12)
            for line in section.content.split('\n'):
                pdf.multi_cell(0, 10, line)
            pdf.ln(5)
        pdf.output(file_path)
        messagebox.showinfo("Export", f"Resume exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeBuilderApp(root)
    root.mainloop()