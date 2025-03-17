import re
import tkinter as tk
import customtkinter
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# Insert brackets
def insert_angle_brackets(line):
    latin_pattern = re.compile(r"[a-zA-Z]")

    if latin_pattern.search(line):
        return f"<{line.strip()}>"
    else:
        return line


# Connect to account
def initialize():
    global driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://kithara.to/login")
    # driver.find_element(By.NAME, "loginName").send_keys("EMAIL")
    # driver.find_element(By.NAME, "loginPass").send_keys("PASSWORD")
    url_input.configure(state="normal")
    url_input.configure(placeholder_text="Enter Artist's URL")
    button_create.configure(state="normal")
    button_clear_url.configure(state="normal")


# Create txt file
def url_create(url, rating):

    global i
    driver.get(url)

    div_elements = driver.find_elements(By.ID, "text")
    class_elements = driver.find_elements(By.CLASS_NAME, "ti")
    artist_elements = driver.find_elements(By.CLASS_NAME, "ar")

    time.sleep(2)
    divs = "\n".join(div.text for div in div_elements)
    tis = "\n".join(class_.text for class_ in class_elements)
    ars = "\n".join(artist.text for artist in artist_elements)

    lines = divs.splitlines()
    processed_lines = [insert_angle_brackets(line) for line in lines]
    final_text = "\n".join(processed_lines)

    folder_path = os.path.join("Guitar Songs/", ars)
    tis = tis + f" ({rating}).txt"
    path = os.path.join(folder_path, tis)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file = open(path, "w", encoding="utf-8")
    file.write(final_text)
    file.close()

    return None


# Keep only the best ratings
def keep_best_ratings(anchor_elements):

    title_list = []
    rating_list = []
    final_list = []
    pattern = r"[-+]?\d*\.?\d+"

    for element in anchor_elements:

        float_element = re.findall(pattern, element.text)

        # If there is a rating
        if float_element:
            rating = float(float_element[0])

            # Keeping only the title
            if "(σ,V," in element.text:
                title = (
                    element.text.replace(float_element[0], "")
                    .replace("(σ,V,)", "")
                    .strip()
                )
            elif "(t,V," in element.text:
                title = (
                    element.text.replace(float_element[0], "")
                    .replace("(t,V,)", "")
                    .strip()
                )
            elif "(V," in element.text:
                title = (
                    element.text.replace(float_element[0], "")
                    .replace("(V,)", "")
                    .strip()
                )
            else:
                title = (
                    element.text.replace(float_element[0], "")
                    .replace("(σ,)", "")
                    .strip()
                )
        else:
            if "(σ,V)" in element.text:
                title = element.text.replace("(σ,V)", "").strip()
            elif "(t,V)" in element.text:
                title = element.text.replace("(t,V)", "").strip()
            elif "(V)" in element.text:
                title = element.text.replace("(V)", "").strip()
            else:
                title = element.text.replace("(σ)", "").strip()
            rating = 0

        final_list.append(element)
        rating_list.append(rating)
        title_list.append(title)

        # Keeping the best rating
        index = title_list.index(title)

        if (rating < 2) & (rating != 0):

            final_list.pop()
            title_list.pop()
            rating_list.pop()
        elif rating_list[index] < rating:

            final_list.pop(index)
            title_list.pop(index)
            rating_list.pop(index)
        elif rating_list[index] > rating:

            final_list.pop()
            title_list.pop()
            rating_list.pop()
        else:
            if title_list.count(title) > 1:

                final_list.pop()
                title_list.pop()
                rating_list.pop()

    return final_list, rating_list


# Get Url and elements
def get_url():

    url = url_input.get()
    driver.get(url)

    url_elements = driver.find_element(By.CLASS_NAME, "tablerev")
    thistfist = url_elements.find_element(By.CLASS_NAME, "thist2col")
    anchor_elements = thistfist.find_elements(By.TAG_NAME, "a")

    if best_rating_check_box.get() == 1:
        best_Rating_list, rating_list = keep_best_ratings(anchor_elements)
        hrefs = [element.get_attribute("href") for element in best_Rating_list]
    else:
        hrefs = [element.get_attribute("href") for element in anchor_elements]

    i = 0
    for url in hrefs:
        url_create(url, rating_list[i])
        i += 1


# Clear the URL input
def clear_url():
    url_input.delete(0, tk.END)


# ---------------- UI -------------------#

# Create the main window
root = customtkinter.CTk()
root.title("Kithara.to Save Chords to txt")
root._set_appearance_mode("system")
root.geometry("450x200")
root.resizable(False, False)
root.iconbitmap("icon.ico")
root.configure(bg="white")


# Initialize button
button_initialize = customtkinter.CTkButton(
    master=root,
    text="Initialize",
    command=initialize,
    width=100,
    height=25,
    border_width=2,
    corner_radius=10,
)
button_initialize.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

# Best rating check box
best_rating_check_box = customtkinter.CTkCheckBox(
    master=root,
    text="Best ratings",
    width=50,
    height=20,
    border_width=2,
    corner_radius=10,
)
best_rating_check_box.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

# URL Entry
url_input = customtkinter.CTkEntry(
    master=root,
    placeholder_text="Enter URL",
    width=300,
    height=25,
    border_width=2,
    corner_radius=10,
    state="disabled",
)
url_input.place(relx=0.5, rely=0.50, anchor=tk.CENTER)

# Save Button
button_create = customtkinter.CTkButton(
    master=root,
    text="Save Chords",
    command=get_url,
    width=100,
    height=25,
    border_width=2,
    corner_radius=10,
    state="disabled",
)
button_create.place(relx=0.2, rely=0.75)

# Clear Button
button_clear_url = customtkinter.CTkButton(
    master=root,
    text="Clear",
    command=clear_url,
    width=100,
    height=25,
    border_width=2,
    corner_radius=10,
    state="disabled",
)
button_clear_url.place(relx=0.57, rely=0.75)

# Start the Tkinter event loop
root.mainloop()
