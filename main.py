import cv2
import mediapipe as mp
import numpy as np
import random
import math
import os
import urllib.request

# Automatically download the required ML model if missing
if not os.path.exists('hand_landmarker.task'):
    print("Downloading MediaPipe Hand Landmarker model (this only happens once)...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        "hand_landmarker.task"
    )

class Particle:
    def __init__(self, x, y, color, size_base, is_anti_gravity):
        self.x = x
        self.y = y
        self.vx = (random.random() - 0.5) * 4.0
        self.vy = (random.random() - 0.5) * 2.0
        self.color = color
        self.size = (random.random() * 3 + 1) * (size_base / 2)
        self.life = 1.0
        self.decay = random.random() * 0.03 + 0.01
        self.is_anti_gravity = is_anti_gravity
        self.is_star = random.random() > 0.5

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.is_anti_gravity:
            self.vy -= 0.15 # Accel up
        else:
            self.vy += 0.15 # Accel down
        
        self.life -= self.decay

def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0)) # BGR

palettes = {
    "Cosmic": [hex_to_bgr("#ff6ef7"), hex_to_bgr("#7ef8ff"), hex_to_bgr("#ffe97e")],
    "Fire": [hex_to_bgr("#ff4444"), hex_to_bgr("#ff9900"), hex_to_bgr("#ffff00")],
    "Ocean": [hex_to_bgr("#00ffaa"), hex_to_bgr("#0088ff"), hex_to_bgr("#aa00ff")],
    "Silver": [hex_to_bgr("#ffffff"), hex_to_bgr("#ddddff"), hex_to_bgr("#aaaaff")],
    "Gold": [hex_to_bgr("#ffd700"), hex_to_bgr("#ff6600"), hex_to_bgr("#ff0066")],
    "Eraser": [(0, 0, 0)]
}

palette_names = list(palettes.keys())
current_palette_idx = 0

brush_sizes = {'S': 1, 'M': 2, 'L': 4}
size_keys = list(brush_sizes.keys())
current_size_idx = 1

is_anti_gravity = True

def main():
    global current_palette_idx, current_size_idx, is_anti_gravity

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam. Please verify webcam access and permissions.")
        return

    # Setup MediaPipe Tasks API (modern, supports ARM64 mac natively)
    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.6,
        min_hand_presence_confidence=0.6,
        min_tracking_confidence=0.6
    )
    
    landmarker = HandLandmarker.create_from_options(options)

    particles = []
    
    ret, frame = cap.read()
    if not ret: return
    h, w, _ = frame.shape
    trail_canvas = np.zeros((h, w, 3), dtype=np.float32)

    smoothed_x, smoothed_y = None, None
    smoothing_factor = 0.4
    last_point = None

    window_name = 'AIR GLITTER - Python Edition'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    def mouse_callback(event, x, y, flags, param):
        global current_palette_idx, current_size_idx, is_anti_gravity
        if event == cv2.EVENT_LBUTTONDOWN:
            if y > h - 80: # Substantially expand the vertical clickable area
                if x < 150: # Toggle gravity
                    is_anti_gravity = not is_anti_gravity
                elif x < 300: # Toggle size
                    current_size_idx = (current_size_idx + 1) % len(size_keys)
                else: # Toggle palette (anywhere to the right)
                    current_palette_idx = (current_palette_idx + 1) % len(palette_names)

    cv2.setMouseCallback(window_name, mouse_callback)

    print("AIR GLITTER Initialized. Press 'c' to clear, 'esc' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1) # Mirror naturally
        
        # Hold text much longer (~1 minute to fade)
        trail_canvas *= 0.998
        
        particle_canvas = np.zeros((h, w, 3), dtype=np.uint8)

        # Process Hands
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        results = landmarker.detect_for_video(mp_image, timestamp_ms)

        if results.hand_landmarks:
            landmarks = results.hand_landmarks[0]
            
            idx_tip = landmarks[8]
            idx_mid = landmarks[6]
            mid_tip = landmarks[12]
            mid_mid = landmarks[10]
            ring_tip = landmarks[16]
            ring_mid = landmarks[14]
            pinky_tip = landmarks[20]
            pinky_mid = landmarks[18]
            palm_center = landmarks[9]

            # Heuristic for an open palm: all four fingers extended upwards
            is_open_palm = (idx_tip.y < idx_mid.y and 
                            mid_tip.y < mid_mid.y and 
                            ring_tip.y < ring_mid.y and 
                            pinky_tip.y < pinky_mid.y)

            # Heuristic for pointing: index is extended, but not all other fingers
            is_pointing = idx_tip.y < idx_mid.y and idx_tip.y < mid_tip.y and not is_open_palm

            if is_open_palm or is_pointing:
                # Use palm center for erasing, index tip for drawing
                target_x = palm_center.x if is_open_palm else idx_tip.x
                target_y = palm_center.y if is_open_palm else idx_tip.y
                
                fx = int(target_x * w)
                fy = int(target_y * h)
                
                # Smooth tracking
                if smoothed_x is None:
                    smoothed_x, smoothed_y = fx, fy
                else:
                    smoothed_x += (fx - smoothed_x) * smoothing_factor
                    smoothed_y += (fy - smoothed_y) * smoothing_factor
                
                currPosX = int(smoothed_x)
                currPosY = int(smoothed_y)
                
                current_pal_name = palette_names[current_palette_idx]
                is_selected_eraser = current_pal_name == "Eraser"
                is_actually_erasing = is_open_palm or is_selected_eraser
                
                if is_open_palm:
                    active_colors = [(0, 0, 0)]
                    brush_radius = 120 # Massive area for palm erasing
                else:
                    active_colors = palettes[current_pal_name]
                    brush_radius = brush_sizes[size_keys[current_size_idx]] * 6
                    if is_selected_eraser:
                        brush_radius *= 3 # Finger eraser is a bit larger

                # Draw continuous trail onto persistent canvas
                if last_point is not None:
                    cv2.line(trail_canvas, (int(last_point[0]), int(last_point[1])), (currPosX, currPosY), active_colors[0], brush_radius)
                
                # Spawn particles along interpolated line
                if last_point and not is_actually_erasing:
                    dist = math.hypot(currPosX - last_point[0], currPosY - last_point[1])
                    steps = max(1, int(dist / 10))
                    for i in range(steps + 1):
                        t = i / steps
                        ix = int(last_point[0] + (currPosX - last_point[0]) * t)
                        iy = int(last_point[1] + (currPosY - last_point[1]) * t)
                        
                        for _ in range(3 * brush_sizes[size_keys[current_size_idx]]):
                            prx = ix + (random.random() - 0.5) * 10
                            pry = iy + (random.random() - 0.5) * 10
                            col = random.choice(active_colors)
                            particles.append(Particle(prx, pry, col, brush_sizes[size_keys[current_size_idx]], is_anti_gravity))

                # Draw physical ring outline to verify the palm is erasing
                if is_open_palm:
                    cv2.circle(frame, (currPosX, currPosY), brush_radius // 2, (200, 200, 200), 2)

                last_point = (currPosX, currPosY)
            else:
                last_point = None
                smoothed_x, smoothed_y = None, None
        else:
            last_point = None
            smoothed_x, smoothed_y = None, None

        # Update and draw particles
        next_particles = []
        for p in particles:
            p.update()
            if p.life > 0:
                next_particles.append(p)
                px, py = int(p.x), int(p.y)
                if 0 <= px < w and 0 <= py < h:
                    if p.is_star:
                        sz = int(p.size * 2)
                        cv2.line(particle_canvas, (px-sz, py), (px+sz, py), p.color, 1)
                        cv2.line(particle_canvas, (px, py-sz), (px, py+sz), p.color, 1)
                    else:
                        cv2.circle(particle_canvas, (px, py), int(p.size), p.color, -1)
        particles = next_particles

        # Blend Canvases
        trail_display = np.clip(trail_canvas, 0, 255).astype(np.uint8)
        
        # Add glow blur
        if trail_display.any():
            trail_display = cv2.GaussianBlur(trail_display, (15, 15), 0)

        # Composite via additive blend (cv2.add avoids overflow but caps at 255 making it glow)
        combined_fx = cv2.add(trail_display, particle_canvas)
        frame = cv2.add(frame, combined_fx)

        # UI Drawing
        ui_y = h - 20
        cv2.putText(frame, f"Gravity: {'OFF (Up)' if is_anti_gravity else 'ON (Down)'}", (20, ui_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Size: {size_keys[current_size_idx]}", (180, ui_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        ui_color = (255,255,255) if palette_names[current_palette_idx] == "Eraser" else palettes[palette_names[current_palette_idx]][0]
        cv2.putText(frame, f"Palette: {palette_names[current_palette_idx]}", (300, ui_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, ui_color, 2)
        cv2.putText(frame, "'c' Clear | 'e' Eraser | ESC Exit", (w - 320, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27: # ESC
            break
        elif key == ord('c'):
            trail_canvas.fill(0)
            particles.clear()
        elif key == ord('e'):
            current_palette_idx = palette_names.index("Eraser")

    landmarker.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
