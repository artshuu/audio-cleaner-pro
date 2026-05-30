import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from processor import AudioProcessor

class AudioCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Audio Cleaner Pro")
        self.geometry("550x300")
        self.resizable(False, False)
        
        self.input_file = None
        self.processor = AudioProcessor()
        
        # Заголовок
        ctk.CTkLabel(self, text="🎙 Очистка аудио от шума и мата", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        # Кнопка загрузки
        self.btn_load = ctk.CTkButton(
            self, text="📂 Загрузить WAV файл", 
            command=self.load_file, height=40
        )
        self.btn_load.pack(pady=10, padx=40, fill="x")
        
        # Статус файла
        self.status_label = ctk.CTkLabel(self, text="Файл не выбран", text_color="gray")
        self.status_label.pack(pady=5)
        
        # Прогресс-бар
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=15)
        self.progress.set(0)
        
        # Кнопка сохранения
        self.btn_save = ctk.CTkButton(
            self, text="💾 Обработать и сохранить", 
            command=self.save_processed, height=40, state="disabled"
        )
        self.btn_save.pack(pady=10, padx=40, fill="x")

    def load_file(self):
        path = filedialog.askopenfilename(
            title="Выберите WAV файл",
            filetypes=[("WAV files", "*.wav")]
        )
        if path:
            self.input_file = path
            self.status_label.configure(text=f"✅ {os.path.basename(path)}", text_color="green")
            self.btn_save.configure(state="normal")
            self.progress.set(0)

    def save_processed(self):
        if not self.input_file:
            return
            
        output_path = filedialog.asksaveasfilename(
            title="Сохранить обработанный файл",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")],
            initialfile=f"cleaned_{os.path.basename(self.input_file)}"
        )
        if not output_path:
            return
            
        # Блокируем кнопки во время обработки
        self.btn_load.configure(state="disabled")
        self.btn_save.configure(state="disabled")
        
        def worker():
            success, msg = self.processor.process(
                self.input_file, 
                output_path,
                progress_cb=lambda v: self.after(0, lambda: self.progress.set(v))
            )
            self.after(0, lambda: self._on_complete(success, msg))
            
        threading.Thread(target=worker, daemon=True).start()

    def _on_complete(self, success, message):
        self.btn_load.configure(state="normal")
        self.btn_save.configure(state="normal")
        if success:
            messagebox.showinfo("Готово", message)
        else:
            messagebox.showerror("Ошибка", message)

if __name__ == "__main__":
    app = AudioCleanerApp()
    app.mainloop()
