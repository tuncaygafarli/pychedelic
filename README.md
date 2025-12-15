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
        variance = np.var(gray)

        edges = cv.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
    
        brightness_std = np.std(gray) / 255.0

        complexity = np.log1p(variance) * 0.5 + edge_density * 0.3 + brightness_std * 0.2

        return complexity
```

Calculate scene complexity score based on image statistical properties.
    
    Mathematical Basis: Uses variance (σ²) to measure scene "busyness":
    - Low variance = Flat, uniform areas (simple effects)
    - High variance = Detailed, textured areas (complex effects)
    
    The complexity score combines three components:
    1. Logarithmic variance term (dominant)
    2. Edge density from Canny edge detection
    3. Normalized brightness standard deviation

## Dynamic Thresholding
```python
self.threshold = np.mean(self.complexities)
```
Statistical Method: Uses mean of recent frame complexities to adapt to different lighting conditions without being affected by outliers.

## Mixture of various mathematical concepts

### Sine Distortion ( using vectorized product )

```python
def sine_distortion(self, frame, time=time.time(), wave_strength=random.randint(10,15), smooth_factor=0.1, speed_factor=2.0):
        h, w = frame.shape[:2]
    
        if not hasattr(self, 'prev_time'):
            self.prev_time = time

        sped_up_time = time * speed_factor

        smoothed_time = self.prev_time * (1 - smooth_factor) + sped_up_time * smooth_factor
        self.prev_time = smoothed_time
        
        y_coords, x_coords = np.indices((h, w)) # using indices instead of nested loops in order to vectorize for performance reasons
        
        wave_x = np.sin(y_coords * 0.05 + smoothed_time) * wave_strength
        wave_y = np.cos(x_coords * 0.05 + smoothed_time) * wave_strength
        
        map_x = np.clip(x_coords + wave_x, 0, w-1).astype(np.float32)
        map_y = np.clip(y_coords + wave_y, 0, h-1).astype(np.float32)
        
        distorted = cv.remap(frame, map_x, map_y, 
                            interpolation=cv.INTER_CUBIC,
                            borderMode=cv.BORDER_REFLECT)
        
        return distorted
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

### Color Bleeding
```python
def _vhs_color_bleeding(self, frame):
        b, g, r = cv.split(frame)
        h, w = r.shape

        for i in range(h):
            shift = 8 + int(np.sin(i * 0.01) * 4)
            r[i] = np.roll(r[i], shift)

            if shift > 0:
                r[i, :shift] = r[i, shift] 
        
            if i % 3 == 0:
                shift_b = -6 + int(np.cos(i * 0.02) * 3)
                b[i] = np.roll(b[i], shift_b)

            if i % 4 == 0:
                shift_g = 2 + int(np.sin(i * 0.01) * 2)
                g[i] = np.roll(g[i], shift_g)
    
        return cv.merge([b, g, r])
```

## Installation
In order to use the library, you need to clone the repository :

```bash
# Clone the repository
git clone https://github.com/tuncayofficial/pychedelic.git

# Navigate to project directory
cd pychedelic

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

It is highly recommended to use a Python virtual environment to isolate your project's dependencies and avoid conflicts with system-wide packages.
### Creating the Virtual Environment
Use the `venv` module, which is built into standard Python installations.
After creation, you must activate the environment before installing any packages (see the all of core dependencies list in `requirements.txt`). Your shell prompt will usually change to show the environment name (e.g., (`venv`)).
| Operating System | Command | Notes |
| :--- | :--- | :--- |
| **Windows** | `python -m venv C:\path\to\your\project\venv` | Use the full path for clarity. `venv` is often the directory name. |
| **Linux / macOS** | `python3 -m venv venv` | We assume `python3` is the executable. Creates a local folder named `venv`. |

---

### Activating the Environment

| Operating System | Command |
| :--- | :--- |
| **Windows (Command Prompt / CMD)** | `C:\path\to\your\project\venv\Scripts\activate.bat` |
| **Windows (PowerShell)** | `C:\path\to\your\project\venv\Scripts\Activate.ps1` |
| **Linux / macOS** | `source venv/bin/activate` |

### Installing dependencies
First, make sure the required packages for your engine are installed inside the new environment:
```bash
pip install -r requirements.txt
```

### Initialize Configuration
If your `config.yaml` file is missing, you'll need to run your initialization command:
```bash
python cli.py --init
```

### Run Your Engine Modes

| Command | Purpose |
| :--- | :--- |
| `python cli.py --mode live` | Starts the program using the default configuration (e.g., webcam ID 0, default module/effect). |
| `python cli.py --mode render --modules VHS` | Processes a video file using the specified module (e.g., applies all of the VHS effects to the default video). |
| `python cli.py --list modules` | Lists available processing modules (e.g., VHS, Tracker, ColorChaos). |
| `python cli.py --list effects` | Lists available processing effects of modules (e.g., rgb_split, vhs_barrel_distortion). |

### Deactivating (When Finished)
When you are done working on the project, simply run:

```bash
deactivate
```
This returns you to your global system Python environment.

### Real-Time Video Processing
Inside the virtual environment, you can run and test various modules and effects of Pychedelic Video Engine.
```bash
python cli.py -mode live --modules ColorChaos # Live processing feed with a general module chain
python cli.py -mode live --modules ColorChaos --effects rgb_split lcd_sine_shift channel_swap # Live processing feed with a defined effect chain
```
_Process video files with live preview and real-time effects!_

### Video Rendering & Export
```bash
python cli.py -mode render --modules VHS # Rendering with a general module chain
python cli.py -mode render --modules VHS --effects vhs_color_bleeding # Rendering with a defined module chain
```
### Debug mode
To debug the process and analyze the results, simply run the commands with `--debug` flag :
```bash
python cli.py -mode webcam --modules Grunge --effects washed_emo_layers --debug
```

## Gallery

![mvclip_channel_shift](https://github.com/user-attachments/assets/b210cc5a-a4c0-4dee-8695-673045d5bc4d) ![artifact_color_chaos (1)](https://github.com/user-attachments/assets/6edd7aa5-6124-4fba-ac6e-70fd887293e6)
![video_2025_11_06_02_15_01](https://github.com/user-attachments/assets/cb2ca4e8-53b9-43b3-a19e-91ae09b55d49) ![1109(1)](https://github.com/user-attachments/assets/9dfe7689-55a3-4724-b2ba-ec411ca38b5d)





## Coming Soon
• Webcam Support - Live camera feed processing ✅

• More Effects - Expanded mathematical transformations

• Audio Integration - Enhanced audio-video synchronization
