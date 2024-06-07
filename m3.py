import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import ttk

# Function to update the video frame in the left panel
def update_video_frame():
    global cap, img, left_canvas

    ret, img = cap.read()

    # Convert to RGB format for MediaPipe
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Hand tracking logic using MediaPipe (replace with your desired processing)
    results = Hands.process(converted_image)  # Placeholder, add hand tracking if needed

    # Clear previous landmarks (optional if not using hand tracking)
    left_canvas.delete("all")

    if results.multi_hand_landmarks:  # Replace with your processing condition if needed
        handNo = 0
        lmList = []

        for id, lm in enumerate(results.multi_hand_landmarks[handNo].landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append((cx, cy))

        for hand_in_frame in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, hand_in_frame, mpHands.HAND_CONNECTIONS)

        # Draw circles around detected landmarks (optional if not using hand tracking)
        for point in lmList:
            cv2.circle(img, point, 5, (0, 255, 0), cv2.FILLED)
            left_canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, fill="green")

    # Convert back to BGR for display
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Update video frame on the left canvas
    photo = tk.PhotoImage(width=img.shape[1], height=img.shape[0], data=img.tostring())
    left_canvas.itemconfig(img_id_left, image=photo)

    # Schedule the next frame update
    root.after(10, update_video_frame)

# Function to update the number display on the right panel
def update_number(number):
    global right_label
    right_label.config(text=number)

# Initialize necessary variables
mpHands = mp.solutions.hands  # Placeholder for hand tracking (if needed)
Hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# Create the main window
root = tk.Tk()
root.title("Hand Tracking Dashboard (Replace with your title)")

# Create left canvas for video frame
left_canvas = tk.Canvas(root, width=320, height=480, bg="gray")
left_canvas.pack(side=tk.LEFT)

# Placeholder image ID for efficient video display
img_id_left = left_canvas.create_image(0, 0, anchor=tk.NW)

# Create right panel for number display
right_frame = tk.Frame(root, bg="lightblue")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Number label on the right
right_label = ttk.Label(right_frame, text="0", font=("Arial", 24), foreground="black")
right_label.pack(pady=20)

# Start button (replace with your trigger for number update)
btn_start = ttk.Button(root, text="Start Tracking (Replace with your button text)", command=lambda: update_number(10))  # Replace 10 with your logic
btn_start.pack(pady=20)

# Close the window when 'q' is pressed
def close_window():
    cap.release()
    root.destroy()

root.bind('<q>', close_window)

# Start the main event loop
root.mainloop()