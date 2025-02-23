import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
import os

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Устанавливаем темную тему
        self.root.configure(bg='#2B2B2B')
        
        # Создаем и настраиваем UI
        self.setup_ui()
        
    def setup_ui(self):
        # Настройка стилей
        style = ttk.Style()
        style.theme_use('clam')  # Используем тему clam как базу
        
        # Настраиваем цвета и стили
        style.configure('Dark.TFrame', background='#2B2B2B')
        style.configure('Dark.TLabel', 
                       background='#2B2B2B', 
                       foreground='#FFFFFF',
                       font=('Helvetica', 12))
        
        style.configure('Dark.TButton',
                       padding=(20, 10),
                       background='#007AFF',
                       foreground='white',
                       font=('Helvetica', 11, 'bold'))
        
        style.map('Dark.TButton',
                  background=[('active', '#0051A8')],
                  foreground=[('active', 'white')])
        
        style.configure('Dark.TEntry',
                       fieldbackground='#3B3B3B',
                       foreground='white',
                       insertcolor='white',
                       font=('Helvetica', 11))
        
        # Создаем основной фрейм
        main_frame = ttk.Frame(self.root, padding="20", style='Dark.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Заголовок
        title_label = ttk.Label(main_frame, 
                               text="Генератор QR кодов",
                               style='Dark.TLabel',
                               font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Поле ввода текста
        input_label = ttk.Label(main_frame,
                               text="Введите текст для QR кода:",
                               style='Dark.TLabel')
        input_label.grid(row=1, column=0, pady=(0, 5), sticky='w')
        
        self.text_input = ttk.Entry(main_frame, 
                                   width=40,
                                   style='Dark.TEntry')
        self.text_input.grid(row=2, column=0, pady=(0, 20), ipady=8)
        
        # Кнопка генерации
        generate_button = ttk.Button(main_frame,
                                   text="Сгенерировать QR код",
                                   command=self.generate_qr,
                                   style='Dark.TButton')
        generate_button.grid(row=3, column=0, pady=(0, 30))
        
        # Место для отображения QR кода
        self.qr_label = ttk.Label(main_frame, style='Dark.TLabel')
        self.qr_label.grid(row=4, column=0, pady=10)
        
    def generate_qr(self):
        text = self.text_input.get().strip()
        if not text:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите текст")
            return
            
        # Создаем QR код
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Создаем изображение
        qr_image = qr.make_image(fill_color="white", back_color="#2B2B2B")
        
        # Сохраняем временно
        if not os.path.exists('qrcodes'):
            os.makedirs('qrcodes')
        
        filename = f"qrcodes/qr_code.png"
        qr_image.save(filename)
        
        # Отображаем в интерфейсе
        image = Image.open(filename)
        image = image.resize((300, 300))  # Увеличиваем размер QR кода
        photo = ImageTk.PhotoImage(image)
        self.qr_label.configure(image=photo)
        self.qr_label.image = photo  # Сохраняем ссылку

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop() 