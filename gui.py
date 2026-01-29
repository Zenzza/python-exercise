import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import comparator
import os

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

class DiffApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QSAI Test 1")
        self.root.geometry("800x600")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1) 

        header_frame = ctk.CTkFrame(root, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        
        header_label = ctk.CTkLabel(header_frame, text="QSAI Test 1", font=ctk.CTkFont(size=24, weight="bold"))
        header_label.pack(pady=15)
        
        btn_frame = ctk.CTkFrame(root, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=20, pady=5)
        
        self.btn_load = ctk.CTkButton(btn_frame, text="Pilih Dokumen", command=self.load_data, font=ctk.CTkFont(size=16))
        self.btn_load.pack()

        self.file_label = ctk.CTkLabel(root, text="Tidak ada dokumen yang di pilih.", text_color="gray")
        self.file_label.grid(row=3, column=0, pady=10)

        table_frame = ctk.CTkFrame(root)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ("kategori", "doc_1", "doc_2", "beda")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        self.tree.heading("kategori", text="Kategori")
        self.tree.heading("doc_1", text="Dokumen Pertama")
        self.tree.heading("doc_2", text="Dokumen Kedua")
        self.tree.heading("beda", text="Perbedaan")
        
        self.tree.column("kategori", width=150)
        self.tree.column("doc_1", width=250)
        self.tree.column("doc_2", width=250)
        self.tree.column("beda", width=150)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", 
                        background="#2b2b2b", 
                        foreground="white", 
                        fieldbackground="#2b2b2b", 
                        font=('Segoe UI', 20), 
                        rowheight=80,
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        
        style.configure("Treeview.Heading", 
                        background="#333333", 
                        foreground="white", 
                        font=('Segoe UI', 30, 'bold'),
                        borderwidth=1,
                        relief="flat")
        
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.parser = comparator.ContentParser()
        self.comparator = comparator.DocumentComparator()

        self.auto_load()

    def auto_load(self):
        doc_a = "Dokumen A.docx"
        doc_b = "Dokumen B.docx"
        if os.path.exists(doc_a) and os.path.exists(doc_b):
            self.run_comparison(os.path.abspath(doc_a), os.path.abspath(doc_b))
        else:
            self.file_label.configure(text="Dokumen tidak ditemukan. Silahkan pilih dokumen dengan benar.")

    def load_data(self):
        file_a = filedialog.askopenfilename(title="Pilih Dokumen Pertama", filetypes=[("Word Documents", "*.docx")])
        if not file_a: return
        
        file_b = filedialog.askopenfilename(title="Pilih Dokumen Kedua", filetypes=[("Word Documents", "*.docx")])
        if not file_b: return
        
        self.run_comparison(file_a, file_b)

    def run_comparison(self, path_a, path_b):
        self.file_label.configure(text=f"Membandingkan: {os.path.basename(path_a)} vs {os.path.basename(path_b)}")
        
        data_a = self.parser.parse_docx(path_a)
        data_b = self.parser.parse_docx(path_b)
        
        if not data_a or not data_b:
            messagebox.showerror("Error", "Gagal membandingkan dokumen.")
            return

        results = self.comparator.compare(data_a, data_b)
        
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        order = [
            "Line Spacing", 
            "Bullet & Numbering", 
            "Spacing Indentasi", 
            "Efek Pencetakan", 
            "Kesalahan Ketik"
        ]
        
        for criteria in order:
            res = results.get(criteria, {"A": "-", "B": "-", "Diff": "-"})
            self.tree.insert("", tk.END, values=(criteria, res["A"], res["B"], res["Diff"]))

if __name__ == "__main__":
    root = ctk.CTk()
    app = DiffApp(root)
    root.mainloop()
