# Pychedelic

A real-time video processing system that applies computer vision techniques and psychedelic effects using mathematical transformations. Transform your webcam feed into a trippy visual experience!

## Features

• Real-time Video Processing - Live webcam feed manipulation
• Auto-calibration - Dynamic threshold detection based on scene complexity
• Psychedelic Effects - Mathematical transformations for trippy visuals
• Modular Architecture - Easy to extend with new effects

## Mathematical Foundations

## Complexity Calculation
```python
def calculate_complexity(self, frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    variance = np.var(gray) # Variation method
    return np.log1p(variance)
```

Mathematical Basis: Uses variance (σ²) to measure how "busy" a scene is:

Low variance = Flat, uniform areas (simple effects)

High variance = Detailed, textured areas (complex effects)

## Dynamic Thresholding
```python
self.threshold = np.median(self.complexities)
```
Statistical Method: Uses median of recent frame complexities to adapt to different lighting conditions without being affected by outliers.

## Mixture of various mathematical concepts

### Sine Distortion ( using vectorized product )

```python
def sine_distortion(self, frame, time, wave_strength=10):
        h, w = frame.shape[:2]
    
        y_coords, x_coords = np.indices((h, w)) # vectorized here
        
        wave_x = np.sin(y_coords * 0.05 + time) * wave_strength
        wave_y = np.cos(x_coords * 0.05 + time) * wave_strength
        
        new_x = np.clip(x_coords + wave_x, 0, w-1).astype(np.int32)
        new_y = np.clip(y_coords + wave_y, 0, h-1).astype(np.int32)
        
        return frame[new_y, new_x]
```

### Hue Shifting
```python
def hue_shift(self, frame, shift_amount):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        hue_channel = hsv[:, :, 0]
        
        hue_channel_int = hue_channel.astype(np.int32)
        new_hue = (hue_channel_int + shift_amount) % 180
        
        hsv[:, :, 0] = new_hue.astype(np.uint8)

        return cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
```

## Installation
In order to use the library, you need to clone the repository :

```bash
# Clone the repository
git clone https://github.com/tuncayofficial/opencv_video_calibration.git

# Navigate to project directory
cd opencv_video_calibration

# Install dependencies
pip install -r requirements.txt
```

## Quick Start
### Real-Time Video Processing
```bash
python main.py -rtm enable --effects ColorChaosManipulator
```
_Process video files with live preview and real-time effects!_

## Gallery

![mvclip_channel_shift](https://github.com/user-attachments/assets/b210cc5a-a4c0-4dee-8695-673045d5bc4d) ![artifact_color_chaos (1)](https://github.com/user-attachments/assets/6edd7aa5-6124-4fba-ac6e-70fd887293e6)
![video_2025_11_06_02_15_01](https://github.com/user-attachments/assets/cb2ca4e8-53b9-43b3-a19e-91ae09b55d49)


### Video Rendering & Export
```bash
python main.py -render enable --effects Calibrator
```
_Render video files with mathematical transformations and export results_

## Coming Soon
• Webcam Support - Live camera feed processing

• More Effects - Expanded mathematical transformations

• Audio Integration - Enhanced audio-video synchronization
