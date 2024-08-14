import cv2
import numpy as np
import time

# Global variables to store the selected HSV range
lower_color = None
upper_color = None
background = None

def select_color(event, x, y, flags, param):
    global lower_color, upper_color
    if event == cv2.EVENT_LBUTTONDOWN:
        frame = param
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        selected_color = hsv[y, x]

        # Set the HSV range with some tolerance
        tolerance = 20  # Reduced tolerance for more precise color selection
        hue = selected_color[0]
        
        # Handle circular hue range
        lower_hue = max(0, hue - tolerance)
        upper_hue = min(179, hue + tolerance)
        
        if upper_hue < lower_hue:
            # When the range crosses the boundary
            lower_color = np.array([0, 50, 50])
            upper_color = np.array([179, 255, 255])
            mask1 = cv2.inRange(hsv, lower_color, np.array([upper_hue, 255, 255]))
            mask2 = cv2.inRange(hsv, np.array([0, 50, 50]), np.array([lower_hue, 255, 255]))
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            lower_color = np.array([lower_hue, 50, 50])
            upper_color = np.array([upper_hue, 255, 255])
            mask = cv2.inRange(hsv, lower_color, upper_color)

        print(f"Selected HSV Range: {lower_color} to {upper_color}")

def create_background(cap, num_frames=30):
    print("Capturing background. Please move out of the frame.")
    backgrounds = []
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            backgrounds.append(frame)
        else:
            print(f"Warning: Could not read frame {i+1}/{num_frames}")
        time.sleep(0.1)
    if backgrounds:
        return np.median(backgrounds, axis=0).astype(np.uint8)
    else:
        raise ValueError("Could not capture any frames for background")

def create_mask(frame, lower_color, upper_color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if lower_color[0] > upper_color[0]:
        lower_color1 = np.array([0, 50, 50])
        upper_color1 = np.array([upper_color[0], 255, 255])
        lower_color2 = np.array([lower_color[0], 50, 50])
        upper_color2 = np.array([179, 255, 255])
        
        mask1 = cv2.inRange(hsv, lower_color1, upper_color1)
        mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Apply morphological operations to refine the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)  # Fill small holes
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)  # Remove noise

    # Apply Gaussian blur to smooth the mask edges
    mask_blur = cv2.GaussianBlur(mask, (15, 15), 0)
    
    return mask_blur

def apply_cloak_effect(frame, mask, background):
    # Normalize the mask to [0, 1] range
    mask_normalized = mask.astype(float) / 255.0
    
    # Create a mask for blending
    mask_inv = 1 - mask_normalized
    
    # Apply the mask to the frame and the background
    fg = frame.astype(float) * mask_inv[:, :, np.newaxis]
    bg = background.astype(float) * mask_normalized[:, :, np.newaxis]
    
    # Blend the foreground and background
    result = cv2.add(fg.astype(np.uint8), bg.astype(np.uint8))
    
    return result

def main():
    global background
    print("OpenCV Version: ", cv2.__version__)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture initial background
    try:
        background = create_background(cap)
    except ValueError as e:
        print(f"Error: {e}")
        cap.release()
        return

    print("Click on the cloak to select the color.")
    cv2.namedWindow("Invisible Cloak")
    
    print("Press 'b' to capture the background.")
    cv2.setMouseCallback("Invisible Cloak", select_color)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            time.sleep(1)
            continue

        # Pass the current frame to the mouse callback
        cv2.setMouseCallback("Invisible Cloak", select_color, param=frame)

        # Update background on 'b' key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('b'):
            try:
                background = create_background(cap)
                print("Background updated.")
            except ValueError as e:
                print(f"Error: {e}")

        if lower_color is not None and upper_color is not None and background is not None:
            mask = create_mask(frame, lower_color, upper_color)
            result = apply_cloak_effect(frame, mask, background)
            cv2.imshow("Invisible Cloak", result)
        else:
            cv2.imshow("Invisible Cloak", frame)

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
