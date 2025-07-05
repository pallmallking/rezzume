import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from sections import SectionManager
from export import export_to_pdf, export_to_docx
from spellcheck import check_spelling
from templates import TEMPLATES, get_template

class ResumeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Word Processor")
        self.sections = SectionManager()
        self.selected_section = None

        self.create_widgets()

    def create_widgets(self):
        # Template selection
        template_frame = tk.Frame(self.root)
        template_frame.pack(fill=tk.X)
        tk.Label(template_frame, text="Template:").pack(side=tk.LEFT)
        self.template_var = tk.StringVar(value="Modern")
        template_menu = ttk.Combobox(template_frame, textvariable=self.template_var, values=list(TEMPLATES.keys()), width=10)
        template_menu.pack(side=tk.LEFT)
        tk.Button(template_frame, text="Load Template", command=self.load_template).pack(side=tk.LEFT)

        # Section List
        self.section_list = tk.Listbox(self.root, width=25)
        self.section_list.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.section_list.bind('<<ListboxSelect>>', self.select_section)

        btn_add = tk.Button(self.root, text="Add Section", command=self.add_section)
        btn_add.pack(side=tk.TOP, padx=5, pady=2)
        btn_remove = tk.Button(self.root, text="Remove Section", command=self.remove_section)
        btn_remove.pack(side=tk.TOP, padx=5, pady=2)

        # Editor
        editor_frame = tk.Frame(self.root)
        editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        toolbar = tk.Frame(editor_frame)
        toolbar.pack(fill=tk.X)
        tk.Button(toolbar, text="Bold", command=self.make_bold).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Italic", command=self.make_italic).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Underline", command=self.make_underline).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Spell Check", command=self.spell_check).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Export PDF", command=self.export_pdf).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Export DOCX", command=self.export_docx).pack(side=tk.LEFT)

        tk.Label(toolbar, text="Font Size:").pack(side=tk.LEFT, padx=5)
        self.font_size_var = tk.IntVar(value=12)
        font_size_menu = ttk.Combobox(toolbar, textvariable=self.font_size_var, values=list(range(8, 25)), width=3)
        font_size_menu.pack(side=tk.LEFT)
        font_size_menu.bind("<<ComboboxSelected>>", self.set_font_size)

        self.text = tk.Text(editor_frame, wrap='word', font=('Arial', 12))
        self.text.pack(fill=tk.BOTH, expand=1)

        btn_save = tk.Button(editor_frame, text="Save Section", command=self.save_section)
        btn_save.pack(fill=tk.X)

        # Track formatting tags for docx export (simple demo)
        self.format_tags = {}

    def load_template(self):
        template = get_template(self.template_var.get())
        self.sections.clear()
        self.section_list.delete(0, tk.END)
        for sec in template:
            self.sections.add(sec["title"])
            self.section_list.insert(tk.END, sec["title"])
        messagebox.showinfo("Template Loaded", f"Loaded template: {self.template_var.get()}")

    def add_section(self):
        title = simpledialog.askstring("Section Title", "Enter section title:")
        if title:
            self.sections.add(title)
            self.section_list.insert(tk.END, title)

    def remove_section(self):
        idx = self.section_list.curselection()
        if idx:
            self.sections.remove(idx[0])
            self.section_list.delete(idx[0])
            self.text.delete(1.0, tk.END)

    def select_section(self, event):
        idx = self.section_list.curselection()
        if not idx:
            return
        self.selected_section = idx[0]
        content, tags = self.sections.get_content(idx[0])
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, content)
        self.format_tags = tags

    def save_section(self):
        if self.selected_section is not None:
            content = self.text.get(1.0, tk.END).strip()
            self.sections.set_content(self.selected_section, content, self.format_tags.copy())
            messagebox.showinfo("Saved", "Section content saved.")

    # Formatting
    def make_bold(self):
        self._tag_selected("bold")
        self.format_tags['bold'] = True

    def make_italic(self):
        self._tag_selected("italic")
        self.format_tags['italic'] = True

    def make_underline(self):
        self._tag_selected("underline")
        self.format_tags['underline'] = True

    def _tag_selected(self, tagname):
        try:
            start = self.text.index(tk.SEL_FIRST)
            end = self.text.index(tk.SEL_LAST)
            self.text.tag_add(tagname, start, end)
            style = tagname
            self.text.tag_configure(tagname, font=('Arial', self.font_size_var.get(), style))
        except tk.TclError:
            pass

    def set_font_size(self, event=None):
        size = self.font_size_var.get()
        self.text.config(font=('Arial', size))

    # Spell Check
    def spell_check(self):
        content = self.text.get(1.0, tk.END)
        misspelled = check_spelling(content)
        if misspelled:
            messagebox.showinfo("Spell Check", f"Misspelled words: {', '.join(misspelled)}")
        else:
            messagebox.showinfo("Spell Check", "No spelling mistakes found.")

    # Export PDF
    def export_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not path:
            return
        export_to_pdf(self.sections.get_all(), path)
        messagebox.showinfo("Export", f"Exported to {path}")

    # Export DOCX
    def export_docx(self):
        path = filedialog.asksaveasfilename(defaultextension=".docx")
        if not path:
            return
        export_to_docx(self.sections.get_all(), path)
        messagebox.showinfo("Export", f"Exported to {path}")