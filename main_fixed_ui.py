import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

class WebScrapingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕷️ Ứng dụng Cào Dữ liệu Web")
        self.root.geometry("800x600")
        self.urls = []
        self.scraped_data = []
        self.setup_ui()

    def setup_ui(self):
        # --- Quản lý URL ---
        url_frame = tk.LabelFrame(self.root, text="📝 Quản lý URL")
        url_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        url_label = tk.Label(url_frame, text="🔗 Nhập URL:")
        url_label.pack(anchor="w", padx=10, pady=(10, 2))

        # Đặt Entry trong một Frame nền trắng để luôn nổi bật
        entry_bg = tk.Frame(url_frame, bg="white", bd=1, relief=tk.SOLID)
        entry_bg.pack(fill="x", padx=10, pady=(0, 10))
        self.url_entry = tk.Entry(entry_bg, font=("Arial", 12), bg="white", fg="black", width=60, relief=tk.FLAT, bd=0)
        self.url_entry.pack(fill="x", padx=2, pady=2)
        self.url_entry.insert(0, "https://example.com")

        btn_frame = tk.Frame(url_frame)
        btn_frame.pack(padx=10, pady=(0, 10), anchor="w")

        add_btn = tk.Button(btn_frame, text="➕ Thêm URL", command=self.add_url)
        add_btn.pack(side="left", padx=(0, 10))
        remove_btn = tk.Button(btn_frame, text="🗑️ Xóa URL", command=self.remove_url)
        remove_btn.pack(side="left")

        listbox_label = tk.Label(url_frame, text="📋 Danh sách URL đã thêm:")
        listbox_label.pack(anchor="w", padx=10)
        self.url_listbox = tk.Listbox(url_frame, height=4, font=("Arial", 10), bg="white", fg="black", relief=tk.SOLID, bd=1)
        self.url_listbox.pack(fill="x", padx=10, pady=(0, 10))

        # --- Cấu hình selector ---
        config_frame = tk.LabelFrame(self.root, text="⚙️ Cấu hình Selector")
        config_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(config_frame, text="📰 CSS Selector cho tiêu đề:").pack(anchor="w", padx=10, pady=(10, 2))
        self.title_selector = tk.Entry(config_frame, font=("Arial", 10), width=40)
        self.title_selector.pack(fill="x", padx=10, pady=(0, 10))
        self.title_selector.insert(0, "h1, .title, .post-title")

        tk.Label(config_frame, text="✏️ CSS Selector cho nội dung:").pack(anchor="w", padx=10, pady=(10, 2))
        self.content_selector = tk.Entry(config_frame, font=("Arial", 10), width=40)
        self.content_selector.pack(fill="x", padx=10, pady=(0, 10))
        self.content_selector.insert(0, ".content, .post-content, article")

        # --- Điều khiển ---
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        self.scrape_button = tk.Button(control_frame, text="🚀 Bắt đầu Cào Dữ liệu", command=self.start_scraping)
        self.scrape_button.pack(side=tk.LEFT, padx=(0, 10))
        self.save_button = tk.Button(control_frame, text="💾 Lưu Excel", command=self.save_to_excel)
        self.save_button.pack(side=tk.LEFT)

        # --- Kết quả ---
        result_frame = tk.LabelFrame(self.root, text="📊 Kết quả Cào dữ liệu")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        columns = ("URL", "Tiêu đề", "Nội dung", "Trạng thái")
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=180)
        self.result_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("✅ Sẵn sàng - Hãy thêm URL và bắt đầu cào dữ liệu!")
        status_bar = tk.Label(self.root, textvariable=self.status_var, anchor="w")
        status_bar.pack(fill=tk.X, padx=20, pady=(0, 5))

    def add_url(self):
        url = self.url_entry.get().strip()
        if url and url != "https://example.com":
            if url not in self.urls:
                self.urls.append(url)
                self.url_listbox.insert(tk.END, url)
                self.url_entry.delete(0, tk.END)
                self.status_var.set(f"✅ Đã thêm URL: {url}")
            else:
                messagebox.showwarning("⚠️ Cảnh báo", "URL này đã tồn tại trong danh sách!")
        else:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng nhập URL hợp lệ!")

    def remove_url(self):
        selection = self.url_listbox.curselection()
        if selection:
            index = selection[0]
            url = self.urls.pop(index)
            self.url_listbox.delete(index)
            self.status_var.set(f"🗑️ Đã xóa URL: {url}")
        else:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng chọn URL cần xóa!")

    def start_scraping(self):
        if not self.urls:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng thêm ít nhất một URL!")
            return
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        for i, url in enumerate(self.urls):
            self.result_tree.insert('', 'end', values=(
                url,
                f"Tiêu đề test #{i+1}",
                f"Nội dung test cho {url} - Đây là dữ liệu mẫu.",
                '✅ Thành công'
            ))
        self.status_var.set(f"🎉 Hoàn thành! Đã xử lý {len(self.urls)} URL.")
        messagebox.showinfo("🎉 Thành công", f"Đã cào dữ liệu từ {len(self.urls)} URL!\n\nĐây là chế độ test. Chức năng scraping thực sẽ được thêm sau.")

    def save_to_excel(self):
        if not self.result_tree.get_children():
            messagebox.showwarning("⚠️ Cảnh báo", "Không có dữ liệu để lưu!")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if filename:
            data = []
            for item in self.result_tree.get_children():
                data.append(self.result_tree.item(item)['values'])
            df = pd.DataFrame(data, columns=["URL", "Tiêu đề", "Nội dung", "Trạng thái"])
            df.to_excel(filename, index=False)
            messagebox.showinfo("💾 Thành công", f"Đã lưu dữ liệu vào file: {filename}")

def main():
    root = tk.Tk()
    app = WebScrapingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 