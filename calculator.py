"""
Advanced Calculator with GUI
Fixed: Now handles chained operations correctly (4+4+4+4+4 = 20)
"""

import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Calculator")
        self.window.geometry("400x600")
        self.window.resizable(False, False)
        self.window.configure(bg='#2c3e50')
        
        # Variables
        self.expression = ""
        self.current_number = ""
        self.result_var = tk.StringVar()
        self.memory = 0
        self.history = []
        self.last_operation = ""
        self.waiting_for_number = False
        
        # Create UI
        self.create_widgets()
        self.bind_keys()
        
    def create_widgets(self):
        """Create all calculator widgets"""
        # Display Frame
        display_frame = tk.Frame(self.window, bg='#34495e', height=150)
        display_frame.pack(fill='both', padx=10, pady=(10, 5))
        display_frame.pack_propagate(False)
        
        # Result Display
        self.result_label = tk.Label(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', 24, 'bold'),
            bg='#34495e',
            fg='white',
            anchor='e',
            padx=10
        )
        self.result_label.pack(fill='both', expand=True)
        
        # Expression Display
        self.expression_label = tk.Label(
            display_frame,
            text='',
            font=('Arial', 12),
            bg='#34495e',
            fg='#bdc3c7',
            anchor='e',
            padx=10
        )
        self.expression_label.pack(fill='x')
        
        # Buttons Frame
        buttons_frame = tk.Frame(self.window, bg='#2c3e50')
        buttons_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Button layout
        buttons = [
            ['MC', 'MR', 'M+', 'M-', '⌫'],
            ['(', ')', 'C', 'CE', '÷'],
            ['7', '8', '9', '×', '√'],
            ['4', '5', '6', '-', 'x²'],
            ['1', '2', '3', '+', '±'],
            ['0', '.', '=', '%', 'H']
        ]
        
        # Create buttons dynamically
        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    font=('Arial', 14, 'bold'),
                    bg='#34495e',
                    fg='white',
                    activebackground='#2c3e50',
                    activeforeground='white',
                    relief='flat',
                    bd=0,
                    command=lambda x=text: self.button_click(x)
                )
                btn.grid(row=row_idx, column=col_idx, padx=3, pady=3, sticky='nsew')
                
                # Style special buttons
                if text in ['=', 'C', 'CE']:
                    btn.configure(bg='#e74c3c')
                elif text in ['MC', 'MR', 'M+', 'M-', 'H']:
                    btn.configure(bg='#8e44ad')
                elif text in ['÷', '×', '-', '+']:
                    btn.configure(bg='#f39c12')
        
        # Configure grid weights
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.grid_columnconfigure(i, weight=1)
    
    def bind_keys(self):
        """Bind keyboard keys to calculator functions"""
        self.window.bind('<Key>', self.key_press)
        self.window.bind('<Return>', lambda e: self.button_click('='))
        self.window.bind('<BackSpace>', lambda e: self.button_click('⌫'))
        self.window.bind('<Escape>', lambda e: self.button_click('C'))
    
    def key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        
        if key.isdigit() or key == '.':
            self.button_click(key)
        elif key in ['+', '-']:
            self.button_click(key)
        elif key == '*':
            self.button_click('×')
        elif key == '/':
            self.button_click('÷')
        elif key == '(' or key == ')':
            self.button_click(key)
        elif key == '%':
            self.button_click('%')
    
    def button_click(self, value):
        """Handle all button clicks"""
        
        # Memory operations
        if value == 'MC':
            self.memory = 0
            return
        elif value == 'MR':
            self.result_var.set(str(self.memory))
            return
        elif value == 'M+':
            try:
                self.memory += float(self.result_var.get())
            except:
                pass
            return
        elif value == 'M-':
            try:
                self.memory -= float(self.result_var.get())
            except:
                pass
            return
        
        # History
        if value == 'H':
            self.show_history()
            return
        
        # Clear operations
        if value == 'C' or value == 'CE':
            self.expression = ""
            self.current_number = ""
            self.result_var.set("")
            self.expression_label.config(text="")
            self.waiting_for_number = False
            return
        
        # Backspace
        if value == '⌫':
            current = self.result_var.get()
            if current:
                self.result_var.set(current[:-1])
            return
        
        # Percentage
        if value == '%':
            try:
                current = float(self.result_var.get())
                self.result_var.set(str(current / 100))
            except:
                pass
            return
        
        # Square root
        if value == '√':
            try:
                current = float(self.result_var.get())
                if current >= 0:
                    self.result_var.set(str(math.sqrt(current)))
                else:
                    messagebox.showerror("Error", "Cannot calculate square root of negative number")
            except:
                pass
            return
        
        # Square
        if value == 'x²':
            try:
                current = float(self.result_var.get())
                self.result_var.set(str(current ** 2))
            except:
                pass
            return
        
        # Negate
        if value == '±':
            try:
                current = self.result_var.get()
                if current and current != '0':
                    if current.startswith('-'):
                        self.result_var.set(current[1:])
                    else:
                        self.result_var.set('-' + current)
            except:
                pass
            return
        
        # Equals
        if value == '=':
            self.calculate_result()
            return
        
        # Handle operators
        if value in ['+', '-', '×', '÷']:
            # If we have a current number, append it to expression
            if self.result_var.get():
                self.expression += self.result_var.get() + " " + value + " "
                self.expression_label.config(text=self.expression)
                self.result_var.set("")
                self.waiting_for_number = True
            # If we're waiting for a number, replace the last operator
            elif self.waiting_for_number and self.expression:
                # Remove last operator and add new one
                parts = self.expression.strip().split()
                if parts:
                    parts[-1] = value
                    self.expression = " ".join(parts) + " "
                    self.expression_label.config(text=self.expression)
            return
        
        # Handle numbers and decimal
        if value.isdigit() or value == '.':
            if self.waiting_for_number:
                # If we just had an operator, start fresh
                self.result_var.set("")
                self.waiting_for_number = False
            
            current = self.result_var.get()
            if value == '.' and '.' in current:
                return
            self.result_var.set(current + value)
            return
        
        # Handle parentheses
        if value in ['(', ')']:
            current = self.result_var.get()
            self.result_var.set(current + value)
            return
    
    def calculate_result(self):
        """Evaluate the expression"""
        try:
            # Build the full expression
            full_expression = self.expression + self.result_var.get()
            
            if not full_expression.strip():
                return
            
            # Replace display symbols with Python operators
            eval_expression = full_expression.replace('×', '*').replace('÷', '/')
            
            # Evaluate
            result = eval(eval_expression)
            
            # Store in history
            self.history.append(f"{full_expression} = {result}")
            
            # Display result
            self.result_var.set(str(result))
            self.expression_label.config(text=full_expression + " =")
            
            # Reset for next calculation
            self.expression = ""
            self.current_number = ""
            self.waiting_for_number = False
            
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero!")
            self.result_var.set("")
            self.expression = ""
            self.waiting_for_number = False
        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {str(e)}")
            self.result_var.set("")
            self.expression = ""
            self.waiting_for_number = False
    
    def show_history(self):
        """Display calculation history"""
        if not self.history:
            messagebox.showinfo("History", "No calculations yet!")
            return
        
        history_text = "\n".join(self.history[-10:])  # Show last 10 entries
        messagebox.showinfo("History (Last 10)", history_text)
    
    def run(self):
        """Start the calculator"""
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()