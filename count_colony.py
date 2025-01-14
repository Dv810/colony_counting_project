import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button, simpledialog
import os



# Function to resize and load an image
def load_and_resize_image(image_path):
    frame = cv2.imread(image_path)
    frame = cv2.resize(frame, (300, 300))

    return frame



# Color detection function
def color_detect(frame):
    def nothing(x):
        pass

    cv2.namedWindow("Color Adjustment")
    
    cv2.createTrackbar("l_color", "Color Adjustment", 0, 255, nothing)
    cv2.createTrackbar("l_shade", "Color Adjustment", 0, 255, nothing)
    cv2.createTrackbar("l_brightness", "Color Adjustment", 0, 255, nothing)
    cv2.createTrackbar("u_color", "Color Adjustment", 255, 255, nothing)
    cv2.createTrackbar("u_shade", "Color Adjustment", 255, 255, nothing)
    cv2.createTrackbar("u_brightness", "Color Adjustment", 255, 255, nothing)
    cv2.resizeWindow("Color Adjustment", 500, 300)

    while True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos("l_color", "Color Adjustment")
        l_s = cv2.getTrackbarPos("l_shade", "Color Adjustment")
        l_v = cv2.getTrackbarPos("l_brightness", "Color Adjustment")

        u_h = cv2.getTrackbarPos("u_color", "Color Adjustment")
        u_s = cv2.getTrackbarPos("u_shade", "Color Adjustment")
        u_v = cv2.getTrackbarPos("u_brightness", "Color Adjustment")

        lower_bound = np.array([l_h, l_s, l_v])
        upper_bound = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow("Original", frame)
        cv2.imshow("Mask", mask)
        cv2.imshow("Result", res)

        key = cv2.waitKey(1)
        if key == ord("s"):
            save_path = os.path.join(os.getcwd(), "mask1.jpg")
            cv2.imwrite(save_path, mask)
            break

    cv2.destroyAllWindows()
    return save_path

# Count white dots function
def count_white_dots(image_path, root):
    while True:
        gray = cv2.imread(image_path, 0)
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        min_area = simpledialog.askinteger("Input", "Enter the minimum value for smaller dot reduce it and If want to avoid very small dot increase it  (default 20):", parent=root, minvalue=1, initialvalue=20)
        if min_area is None:
            min_area = 20
        max_area = 500

        filtered_contours = [cnt for cnt in contours if min_area < cv2.contourArea(cnt) < max_area]
        output_image = cv2.imread(image_path)
        cv2.drawContours(output_image, filtered_contours, -1, (0, 255, 0), 1)

        cv2.imshow("White Dots", output_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        satisfied = simpledialog.askstring("Result", f"Number of white dots: {len(filtered_contours)}. Are you satisfied with the result? (yes/no):", parent=root)
        if satisfied and satisfied.strip().lower() == "yes":
            return len(filtered_contours)

# Tkinter GUI Application
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        frame = load_and_resize_image(file_path)
        mask_path = color_detect(frame)
        num_white_dots = count_white_dots(mask_path, root)
        result_label.config(text=f"Number of white dots: {num_white_dots}")

# Main GUI Window
root = tk.Tk()
root.title("Main")
root.resizable(height = None, width = None)

label = Label(root, text="Color Detection and White Dot Counter", font=("Helvetica", 14))
label.pack(pady=10)

button = Button(root, text="Open Image", command=open_file, font=("Helvetica", 12))
button.pack(pady=10)

result_label = Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

root.mainloop()
