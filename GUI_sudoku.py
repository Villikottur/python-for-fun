# Import tkinter module
import tkinter as tk
from tkinter import messagebox
from tkinter.constants import Y
from tkinter import filedialog

# F to set GUIs grid
def set_GUI():
    for x in range(13):
        for y in range(13):
            if y in [0, 4, 8, 12] and x not in [0, 4, 8, 12]:
                frame = tk.Frame(window, bg = "black", width = 5, height = 45)
                frame.grid(row = x, column = y)
            elif x in [0, 4, 8, 12] and y not in [0, 4, 8, 12]:
                frame = tk.Frame(window, bg = "black", width = 48, height = 5)
                frame.grid(row = x, column = y)
            elif x in [0, 4, 8, 12] and y in [0, 4, 8, 12]:
                frame = tk.Frame(window, bg = "black", width = 5, height = 5)
                frame.grid(row = x, column = y)
            else:
                if x <= 3:
                    cell = tk.Entry(window, width = 2, font = ("Verdana", 25), justify = "center")
                    cell.grid(row = x, column = y)
                    sudoku[x-1].append(cell)
                elif 5 <= x <= 7:
                    cell = tk.Entry(window, width = 2, font = ("Verdana", 25), justify = "center")
                    cell.grid(row = x, column = y)
                    sudoku[x-2].append(cell)
                else:
                    cell = tk.Entry(window, width = 2, font = ("Verdana", 25), justify = "center")
                    cell.grid(row = x, column = y)
                    sudoku[x-3].append(cell)
    # Solve button
    solve_but = tk.Button(window, width = 6, height = 2, font = ("Cantarell", 11), text = "Solve", relief = "raised", command = press_but)
    solve_but.place(x = 45, y = 430)
    # Reset button
    reset_but = tk.Button(window, width = 6, height = 2, font = ("Cantarell", 11), text = "Reset", relief = "raised", command = reset_grid)
    reset_but.place(x = 145, y = 430)
    # Save button
    save_but = tk.Button(window, width = 6, height = 2, font = ("Cantarell", 11), text = "Save", relief = "raised", command = save_sudoku)
    save_but.place(x = 245, y = 430)
    # Load button
    load_but = tk.Button(window, width = 6, height = 2, font = ("Cantarell", 11), text = "Load", relief = "raised", command = load_sudoku)
    load_but.place(x = 345, y = 430)

# F to reset grid
def reset_grid():
    for x in range(9):
        for y in range(9):
            sudoku[x][y].delete(0, "end")
            sudoku[x][y].config(fg = "black")  

# F to save sudoku as txt file
def save_sudoku():
    file = filedialog.asksaveasfile(title="Select a file", filetypes=[("Text Files", "*.txt")], defaultextension=".txt", mode='w')
    if file:  
            for x in range(9):
                for y in range(9):
                    if sudoku[x][y].get() == "":
                        file.write("[0] ")
                    else:
                        file.write("["+sudoku[x][y].get()+"] ")
            file.close()
    
# F to load sudoku from txt file
def load_sudoku():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text Files", "*.txt")])
    
    if file_path:
        with open(file_path, "r") as file:
            content = file.read().strip()
            numbers = content.replace('[', '').replace(']', '').split()

            if len(numbers) > 81:
                messagebox.showwarning("Invalid file", "Please check the file you selected contains 81 numbers max.")
                return
            
            index = 0
            for x in range(9):
                for y in range(9):
                    try:
                        if numbers[index] == "0":
                            sudoku[x][y].delete(0, "end")
                            sudoku[x][y].insert(0, "")
                            index += 1
                        else:
                            sudoku[x][y].delete(0, "end")
                            sudoku[x][y].insert(0, numbers[index])
                            index += 1
                    except IndexError as e:
                        return
                    
# F to validate values from input
def validate_values():
    for x in range(9):
        for y in range(9):
            if len(sudoku[x][y].get()) > 1 or sudoku[x][y].get() == "0" or (len(sudoku[x][y].get()) != 0 and sudoku[x][y].get().isdigit() == False):
                messagebox.showwarning("Invalid input", "Please use numbers only, and make sure they're all between 1 and 9 with no spaces")
                return False

# F to make sure no double nums in columns, rows, boxes
def no_double():
    for x in range(9):
        for y in range(9):
            if sudoku[x][y].get().isdigit():
                # Rows
                for xx in range(9):
                    if xx == x:
                        continue
                    elif sudoku[x][y].get() == sudoku[xx][y].get():
                        print(sudoku[xx][y].get())
                        messagebox.showwarning("Invalid input", "Please check that there are no doubles in the same row")
                        return False
                # Columns
                for yy in range(9):
                    if yy == y:
                        continue
                    elif sudoku[x][y].get() == sudoku[x][yy].get():
                        print(sudoku[x][yy].get())
                        messagebox.showwarning("Invalid input", "Please check that there are no doubles in the same column")
                        return False
                # Boxes
                box_x = (x // 3) * 3
                box_y = (y // 3) * 3
                for i in range(box_x, box_x + 3):
                    for j in range(box_y, box_y + 3):
                        if (0 <= i < 9) and (0 <= j < 9) and (i != x or j != y) and sudoku[i][j].get() == sudoku[x][y].get():
                            messagebox.showwarning("Invalid input", "Please check that there are no doubles in the same box")
                            return False
    return True

# F to make sure no totally empty cells
def no_empty():
    count = 0
    for x in range(9):
        for y in range(9):
            if sudoku[x][y].get() == "":
                count += 1
    if count == 81:
        messagebox.showwarning("No valid input", "Please make sure to enter at least one number")
        return False
    else:
        return True

# F to make sure no totally filled in cells
def no_full():
    count = 0
    for x in range(9):
        for y in range(9):
            if sudoku[x][y].get() != "":
                count += 1
    if count == 81:
        messagebox.showinfo("Uhm...", "Seems like this sudoku is already complete")
        return False
    else:
        return True

# F to find empty cell
def find_empty():
    for x in range(9):
        for y in range(9):
            if sudoku[x][y].get() == "":
                return (x, y)
    return False

# F to get if num in col
def num_in_col(y, num):
    for x in range(9):
        if sudoku[x][y].get() == str(num):
            return True
    return False

# F to get if num in row
def num_in_row(x, num):
    for y in range(9):
        if sudoku[x][y].get() == str(num):
            return True
    return False

# F to get if num in box
def num_in_box(xbox, ybox, num):
    for x in range(3):
        for y in range(3):
            if sudoku[x + xbox][y + ybox].get() == str(num):
                return True
    return False

# F to validate cell
def validate_cell(x, y, num):
    return not (num_in_row(x, num)) and not (num_in_col(y, num)) and not (num_in_box(x - (x % 3), y - (y % 3), num))

# F to solve and display puzzle
def solve_sudoku():
    find = find_empty()
    if not find_empty():
        return True
    else:
        x, y = find
    for num in range(1, 10):
        if validate_cell(x, y, num):
            sudoku[x][y].delete(0, "end")
            sudoku[x][y].insert(0, str(num))
            sudoku[x][y].config(fg = "SpringGreen3")
            window.update_idletasks()
            if solve_sudoku():
                return True
            sudoku[x][y].delete(0, "end")   
    return False
                    
# F for solve button
def press_but():
    if (validate_values() != False) and (no_double() != False) and (no_empty() == True) and (no_full() == True):
        solve_sudoku()

# --- Main ---
if __name__ == "__main__":
    # Set window
    window = tk.Tk() 
    window.title("Sudoku solver")
    window.geometry("452x490")
    window.resizable(False, False)

    # Set sudoku
    sudoku = [[] for _ in range(9)]

    # Set GUIs grid
    set_GUI()

    # Keep the app running
    window.mainloop()