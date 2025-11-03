# OpenCV Video Calibration & Psychedelic Effects

A real-time video processing system that applies computer vision techniques and psychedelic effects using mathematical transformations. Transform your webcam feed into a trippy visual experience! 🌈✨

## 🌟 Features

• 🎥 Real-time Video Processing - Live webcam feed manipulation
• ⚡ Auto-calibration - Dynamic threshold detection based on scene complexity
• 🌊 Psychedelic Effects - Mathematical transformations for trippy visuals
• 🧩 Modular Architecture - Easy to extend with new effects

## 🧮 Mathematical Foundations

## Complexity Calculation
```python
def calculate_complexity(self, frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    return np.var(gray)
```
Mathematical Basis: Uses variance (σ²) to measure how "busy" a scene is:

Low variance = Flat, uniform areas (simple effects)

High variance = Detailed, textured areas (complex effects)

Dynamic Thresholding
```python
self.threshold = np.median(self.complexities)
Statistical Method: Uses median of recent frame complexities to adapt to different lighting conditions without being affected by outliers.
```
