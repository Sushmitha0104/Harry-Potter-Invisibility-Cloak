# Invisibility Cloak using OpenCV

## Overview
This project implements the famous "Invisibility Cloak" effect from the Harry Potter series using OpenCV in Python. By capturing the background and creating a mask based on a selected color (the cloak), the cloak area is replaced with the background, creating an illusion of invisibility. The model is fine-tuned to handle a variety of color ranges, ensuring accuracy and smoothness in the effect.

## Features
- **Real-Time Cloak Detection**: Identifies and masks the selected cloak color in real time.
- **Background Capture**: Captures the background frame before the cloak is introduced.
- **Smooth Transitions**: Utilizes morphological operations and Gaussian blurring to ensure smooth edges and reduce noise in the mask.
- **Highly Accurate**: Achieves a high accuracy rate in detecting the cloak and applying the effect smoothly.

## Requirements
- Python 3.x
- OpenCV
- NumPy

You can install the required packages using pip:

```bash
pip install opencv-python numpy
```

## How to Run the Project
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sushmitha0104/Harry-Potter-Invisibility-Cloak.git
   cd invisibility-cloak
   ```

2. **Run the script**:
   ```bash
   python main.py
   ```

3. **Use the Project**:
    - Run the script to open the webcam feed.
    - Press the 'b' key to capture the plain background without any objects or cloak in the frame. This captured background will be used to replace the selected cloak area.
    - After capturing the background, wear the cloak and introduce other objects if needed.
    - Click on the cloak in the video feed to select the color you want to make invisible. The script will create a mask for the selected color and apply the invisibility effect.
    - If the background changes, press the 'b' key to re-capture the background and ensure the effect remains consistent.

4. **Exit the application**:
   - Press 'q' to quit the application.

## File Structure
- `main.py`: The main script to run the invisibility cloak effect.
- `README.md`: This file, providing an overview of the project.

## How It Works
1. **Background Capture**: The background is captured without the cloak, allowing it to be used as the replacement for the cloak area.
2. **Color Selection**: The user clicks on the color to be made invisible. The script then identifies this color in the HSV color space.
3. **Mask Creation**: A mask is created based on the selected color, highlighting areas to be replaced by the background.
4. **Morphological Operations**: The mask is refined using closing, opening, and Gaussian blur operations to ensure a smooth and accurate effect.
5. **Apply the Effect**: The final effect is applied by combining the masked area with the background.

## Known Issues
- **Lighting Conditions**: The effect may vary under different lighting conditions. Adjust the tolerance level if needed.
- **Complex Backgrounds**: Highly complex or dynamic backgrounds might reduce the effectiveness of the cloak effect.

## Contributions
Feel free to fork this project, create issues, or submit pull requests. Contributions are welcome!

## License
This project is licensed under the MIT License.

