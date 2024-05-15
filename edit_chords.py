import re
import tkinter as tk
import customtkinter
import os
import time
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

last_slider_value = 0
first_slider = True
original_chords_text = []


def insert_angle_brackets(line):
    latin_pattern = re.compile(r"[a-zA-Z]")

    if latin_pattern.search(line):
        return f"< {line.strip()} >"
    else:
        return line


def process_text_and_display():

    global last_slider_value
    global first_slider

    input_text = modify_input.get("1.0", tk.END)
    final_chords_label.delete("1.0", tk.END)
    lines = input_text.splitlines()
    processed_lines = [insert_angle_brackets(line) for line in lines]
    output_text = "\n".join(processed_lines)
    final_chords_label.delete("1.0", tk.END)
    final_chords_label.insert("1.0", output_text)
    modify_input.delete("1.0", tk.END)
    transpose_chords_slider.set(0)
    last_slider_value = 0
    first_slider = True


def copy():
    final_chords_label.clipboard_clear()
    final_chords_label.clipboard_append(final_chords_label.get("1.0", tk.END))


def save_output_to_file():
    output_text = final_chords_label.get("1.0", tk.END)
    print(output_text)
    if output_text != "\n":
        output_file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        )

        if output_file_path:
            with open(output_file_path, "w", encoding="utf-8") as outfile:
                outfile.write(output_text)
            print(f"Output saved to {output_file_path}")
            final_chords_label.delete("1.0", tk.END)

            return
    else:
        print("No output to save.")

    transpose_chords_slider.set(0)


def clear():
    modify_input.delete("1.0", tk.END)


def clear_all():
    modify_input.delete("1.0", tk.END)
    final_chords_label.delete("1.0", tk.END)
    transpose_chords_slider.set(0)


def slider(value):
    global last_slider_value
    global first_slider
    global original_chords_text
    print(int(value))

    if first_slider:

        original_chords_text = final_chords_label.get("1.0", tk.END)
        transposed_text = transpose_chords(original_chords_text, int(value))
        final_chords_label.delete("1.0", tk.END)
        final_chords_label.insert("1.0", transposed_text)
        last_slider_value = int(value)
        first_slider = False
    elif int(value) == 0:

        final_chords_label.delete("1.0", tk.END)
        final_chords_label.insert("1.0", original_chords_text)
        last_slider_value = int(value)
    elif last_slider_value != int(value):

        transposed_text = transpose_chords(original_chords_text, int(value))
        final_chords_label.delete("1.0", tk.END)
        final_chords_label.insert("1.0", transposed_text)
        last_slider_value = int(value)


def transpose_chords(text, semitones):

    global original_chords
    # Define the chord dictionary
    major = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    minor = [
        "Cm",
        "C#m",
        "Dm",
        "D#m",
        "Em",
        "Fm",
        "F#m",
        "Gm",
        "G#m",
        "Am",
        "A#m",
        "Bm",
    ]
    # Transpose each chord
    transposed_text = ""
    for line in text.splitlines():
        words = re.findall(r"[\b\w+#\w+\b|\b\w+\b]+", line)
        print(f"Found words : {words}")
        if line[0] == "<":
            transposed_line = ""
            for i in range(len(words)):
                if i == 0:
                    if words[i] in major:
                        index = major.index(words[i])
                        new_index = (index + semitones) % 12
                        transposed_word = major[new_index]
                        transposed_line = line.replace(words[0], transposed_word)
                    elif words[i] in minor:
                        index = minor.index(words[i])
                        new_index = (index + semitones) % 12
                        transposed_word = minor[new_index]
                        transposed_line = line.replace(words[0], transposed_word)
                    else:
                        transposed_word = ""
                    print(
                        f"For {words[i]} word ----- new word : {transposed_word} ----- final line : {transposed_line}"
                    )
                elif words[i] in major:
                    index = major.index(words[i])
                    new_index = (index + semitones) % 12
                    transposed_word = major[new_index]
                    transposed_line = transposed_line.replace(words[i], transposed_word)
                    print(
                        f"For {words[i]} word ----- new word : {transposed_word} ----- final line : {transposed_line}"
                    )
                elif words[i] in minor:
                    index = minor.index(words[i])
                    new_index = (index + semitones) % 12
                    transposed_word = minor[new_index]
                    transposed_line = transposed_line.replace(words[i], transposed_word)
                    print(
                        f"For {words[i]} word ----- new word : {transposed_word} ----- final line : {transposed_line}"
                    )
                else:
                    transposed_line = transposed_line + ""
            transposed_text += transposed_line + "\n"
        else:
            transposed_text += line + "\n"
    return transposed_text


# Create the main window
root = customtkinter.CTk()
root.title("Text Processor with GUI")
root.geometry("600x650")
root.iconbitmap("icon.ico")
root.resizable(False, False)


# Text Modification

# Input-to-modify textbox
modify_input = customtkinter.CTkTextbox(
    master=root,
    width=400,
    height=220,
    border_width=2,
    corner_radius=10,
)
modify_input.place(
    relx=0.16,
    rely=0.02,
)

# Modify Button
modify_button = customtkinter.CTkButton(
    master=root,
    text="Modify",
    command=process_text_and_display,
    width=100,
    height=25,
    border_width=2,
    corner_radius=10,
)
modify_button.place(relx=0.22, rely=0.38)

# Clear Button
button_clear_chords = customtkinter.CTkButton(
    master=root,
    text="Clear",
    command=clear,
    width=100,
    height=25,
    border_width=2,
    corner_radius=10,
)
button_clear_chords.place(relx=0.6, rely=0.38)

# Final chord textBox
final_chords_label = customtkinter.CTkTextbox(
    master=root,
    width=400,
    height=220,
    border_width=2,
    corner_radius=10,
)
final_chords_label.place(
    relx=0.16,
    rely=0.44,
)

# Transpose Chords Slider
transpose_chords_slider = customtkinter.CTkSlider(
    master=root,
    from_=-6,
    to=6,
    number_of_steps=12,
    progress_color="green",
    width=350,
    command=slider,
)
transpose_chords_slider.place(relx=0.2, rely=0.8)

# Label -6 to +6 for slider
label_6 = customtkinter.CTkLabel(
    master=root,
    text="-6      -5      -4      -3     -2     -1       0     +1      +2    +3    +4    +5     +6 ",
    width=200,
)
label_6.place(relx=0.2, rely=0.825)

# Copy Button
button_copy = customtkinter.CTkButton(
    master=root,
    text="Copy text",
    command=copy,
    width=100,
    height=25,
    border_width=2,
    corner_radius=10,
)
button_copy.place(relx=0.21, rely=0.87)

# Save to file Button
button_save = customtkinter.CTkButton(
    master=root,
    text="Save to txt file",
    command=save_output_to_file,
    width=100,
    height=25,
    border_width=2,
    corner_radius=10,
)
button_save.place(relx=0.6, rely=0.87)

# Clear All Button
button_clear_all = customtkinter.CTkButton(
    master=root,
    text="Clear ALL",
    command=clear_all,
    width=100,
    height=25,
    border_width=2,
    corner_radius=10,
)
button_clear_all.place(relx=0.405, rely=0.94)

# Start the Tkinter event loop
root.mainloop()
