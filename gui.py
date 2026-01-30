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
        
        header_label = ctk.CTkLabel(header_frame, text="Pembanding Dokumen", font=ctk.CTkFont(size=24, weight="bold"))
        header_label.pack(pady=15)
        
        btn_frame = ctk.CTkFrame(root, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=20, pady=5)
        
        self.btn_load = ctk.CTkButton(btn_frame, text="Pilih Dokumen", command=self.load_data, font=ctk.CTkFont(size=16))
        self.btn_load.pack()

        self.file_label = ctk.CTkLabel(root, text="Tidak ada dokumen yang di pilih.", text_color="gray")
        self.file_label.grid(row=3, column=0, pady=10)

        self.table_container = ctk.CTkFrame(root)
        self.table_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.table_container.grid_columnconfigure(0, weight=1)
        self.table_container.grid_rowconfigure(1, weight=1) 

        self.header_bg = ctk.CTkFrame(self.table_container, corner_radius=0, fg_color="#333333")
        self.header_bg.grid(row=0, column=0, sticky="ew")
        self.header_bg.grid_columnconfigure(0, weight=2) 
        self.header_bg.grid_columnconfigure(1, weight=3) 
        self.header_bg.grid_columnconfigure(2, weight=3) 
        self.header_bg.grid_columnconfigure(3, weight=2) 
        
        headers = ["Kategori", "Dokumen Pertama", "Dokumen Kedua", "Perbedaan"]
        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(self.header_bg, text=h, font=("Segoe UI", 16, "bold"), text_color="white")
            lbl.grid(row=0, column=i, padx=10, pady=10, sticky="ew")

        self.table_content = ctk.CTkScrollableFrame(self.table_container, corner_radius=0, fg_color="transparent")
        self.table_content.grid(row=1, column=0, sticky="nsew")
        self.table_content.grid_columnconfigure(0, weight=2)
        self.table_content.grid_columnconfigure(1, weight=3)
        self.table_content.grid_columnconfigure(2, weight=3)
        self.table_content.grid_columnconfigure(3, weight=2)
        
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
        self.file_label.configure(text=f"Membandingkan: {os.path.basename(path_a)} dengan {os.path.basename(path_b)}")
        
        data_a = self.parser.parse_docx(path_a)
        data_b = self.parser.parse_docx(path_b)
        
        if not data_a or not data_b:
            messagebox.showerror("Error", "Gagal membandingkan dokumen.")
            return

        results = self.comparator.compare(data_a, data_b)
        
        for widget in self.table_content.winfo_children():
            widget.destroy()
            
        order = [
            "Line Spacing", 
            "Bullet & Numbering", 
            "Spacing Indentasi", 
            "Efek Pencetakan", 
            "Kesalahan Ketik"
        ]
        
        row_idx = 0
        for criteria in order:
            res = results.get(criteria, {"A": "-", "B": "-", "Diff": "-"})
            vals = [criteria, res["A"], res["B"], res["Diff"]]
            
            bg_color = "#2b2b2b" if row_idx % 2 == 0 else "#2b2b2b" 
            
            for col_idx, text in enumerate(vals):
                w_len = 200
                if col_idx == 1 or col_idx == 2: w_len = 250
                
                lbl = ctk.CTkLabel(
                    self.table_content, 
                    text=str(text), 
                    font=("Segoe UI", 14), 
                    text_color="white",
                    wraplength=w_len,
                    justify="left",
                    anchor="w"
                )
                lbl.grid(row=row_idx, column=col_idx, sticky="ew", padx=5, pady=5)
                
            separator = ctk.CTkFrame(self.table_content, height=2, fg_color="#444444")
            separator.grid(row=row_idx+1, column=0, columnspan=4, sticky="ew", pady=(5,0))

            row_idx += 2 

if __name__ == "__main__":
    root = ctk.CTk()
    app = DiffApp(root)
    root.mainloop()

