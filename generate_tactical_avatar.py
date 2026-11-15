import os
import sys
import math
import random
import cv2
import numpy as np

# Config
SRC_DEV = r"C:/Users/Ishan Gupta/.gemini/antigravity/brain/f219f84d-6b0d-4d5d-abc9-5bc17968166b/.user_uploaded/media_1794754435456_6d5e1085.jpg"
SRC_OP = r"C:/Users/Ishan Gupta/.gemini/antigravity/brain/f219f84d-6b0d-4d5d-abc9-5bc17968166b/.user_uploaded/media_1794754455079_4f6add92.jpg"
OUT_DIR = r"C:\Users\Ishan Gupta\.gemini\antigravity\scratch\github-profile\assets"
FRAMES_DIR = r"C:\Users\Ishan Gupta\.gemini\antigravity\scratch\github-profile\avatar_frames"
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

SIZE = 360
CX, CY = SIZE // 2, SIZE // 2
RADIUS = SIZE // 2 - 4 # 176 px
TOTAL_FRAMES = 120
FPS = 24

# Load & resize
im_dev_raw = cv2.imread(SRC_DEV)
im_op_raw = cv2.imread(SRC_OP)

im_dev = cv2.resize(im_dev_raw, (SIZE, SIZE), interpolation=cv2.INTER_LANCZOS4)
im_op = cv2.resize(im_op_raw, (SIZE, SIZE), interpolation=cv2.INTER_LANCZOS4)

# Create circular mask
circle_mask = np.zeros((SIZE, SIZE), dtype=np.uint8)
cv2.circle(circle_mask, (CX, CY), RADIUS, 255, -1)

# Precompute Canny edges
gray_dev = cv2.cvtColor(im_dev, cv2.COLOR_BGR2GRAY)
gray_op = cv2.cvtColor(im_op, cv2.COLOR_BGR2GRAY)
edges_dev = cv2.Canny(gray_dev, 45, 120)
edges_op = cv2.Canny(gray_op, 45, 120)

def apply_chromatic_aberration(img, offset_x):
    if offset_x == 0:
        return img
    b, g, r = cv2.split(img)
    M_b = np.float32([[1, 0, offset_x], [0, 1, 0]])
    M_r = np.float32([[1, 0, -offset_x], [0, 1, 0]])
    b_s = cv2.warpAffine(b, M_b, (SIZE, SIZE), borderMode=cv2.BORDER_REFLECT)
    r_s = cv2.warpAffine(r, M_r, (SIZE, SIZE), borderMode=cv2.BORDER_REFLECT)
    return cv2.merge([b_s, g, r_s])

def apply_slice_glitch(img, intensity=1.0):
    out = img.copy()
    num_slices = random.randint(3, 7)
    for _ in range(num_slices):
        y = random.randint(30, SIZE - 50)
        h = random.randint(4, 18)
        shift = int(random.uniform(-16, 16) * intensity)
        if shift != 0:
            strip = out[y:y+h, :].copy()
            M = np.float32([[1, 0, shift], [0, 1, 0]])
            out[y:y+h, :] = cv2.warpAffine(strip, M, (SIZE, h), borderMode=cv2.BORDER_REFLECT)
    return out

def draw_tactical_hud(img, mode="DEV", frame_idx=0, notice=None):
    overlay = img.copy()
    
    # 1. CRT Scanlines
    scanlines = np.zeros_like(img)
    for y in range(0, SIZE, 3):
        scanlines[y, :] = (14, 14, 14)
    overlay = cv2.subtract(overlay, scanlines)
    
    # Colors (BGR)
    color_cyan = (255, 230, 0)      # #00E6FF
    color_emerald = (80, 220, 50)    # #32DC50
    color_crimson = (40, 50, 240)    # #F03228
    color_amber = (0, 180, 255)      # #FFB400
    color_white = (245, 245, 245)
    
    hud_color = color_cyan if mode == "DEV" else color_emerald
    if "TRANS" in mode:
        hud_color = color_amber if random.random() > 0.4 else color_cyan
        
    font_mono = cv2.FONT_HERSHEY_PLAIN
    
    # 2. Outer Tactical Radar Ring
    cv2.circle(overlay, (CX, CY), RADIUS - 2, hud_color, 1, lineType=cv2.LINE_AA)
    cv2.circle(overlay, (CX, CY), RADIUS - 6, (40, 40, 40), 1, lineType=cv2.LINE_AA)
    
    # 3. Tactical Cardinal Notches (0°, 90°, 180°, 270°)
    notch_len = 10
    # Top
    cv2.line(overlay, (CX, CY - RADIUS + 2), (CX, CY - RADIUS + 2 + notch_len), hud_color, 2, cv2.LINE_AA)
    # Bottom
    cv2.line(overlay, (CX, CY + RADIUS - 2), (CX, CY + RADIUS - 2 - notch_len), hud_color, 2, cv2.LINE_AA)
    # Left
    cv2.line(overlay, (CX - RADIUS + 2, CY), (CX - RADIUS + 2 + notch_len, CY), hud_color, 2, cv2.LINE_AA)
    # Right
    cv2.line(overlay, (CX + RADIUS - 2, CY), (CX + RADIUS - 2 - notch_len, CY), hud_color, 2, cv2.LINE_AA)
    
    # 4. Rotating Tactical Radar Sweep
    angle_rad = (frame_idx * 2 * math.pi / 60) # 1 full rotation every 60 frames (2.5s)
    radar_len = RADIUS - 12
    rx = int(CX + radar_len * math.cos(angle_rad))
    ry = int(CY + radar_len * math.sin(angle_rad))
    cv2.line(overlay, (CX, CY), (rx, ry), hud_color, 1, cv2.LINE_AA)
    
    # 5. In-Circle Text Telemetry
    if mode == "DEV":
        # Header Badge
        header_text = "ISHAN // DEV_CORE"
        t_sz = cv2.getTextSize(header_text, font_mono, 0.9, 1)[0]
        tx = CX - t_sz[0] // 2
        # Dark pill backdrop
        cv2.rectangle(overlay, (tx - 6, 26), (tx + t_sz[0] + 6, 46), (15, 20, 25), -1)
        cv2.rectangle(overlay, (tx - 6, 26), (tx + t_sz[0] + 6, 46), hud_color, 1)
        cv2.putText(overlay, header_text, (tx, 41), font_mono, 0.9, color_white, 1, cv2.LINE_AA)
        
        # Footer Badge
        footer_text = "STATUS: NOMINAL"
        f_sz = cv2.getTextSize(footer_text, font_mono, 0.85, 1)[0]
        fx = CX - f_sz[0] // 2
        cv2.rectangle(overlay, (fx - 6, SIZE - 46), (fx + f_sz[0] + 6, SIZE - 26), (15, 20, 25), -1)
        cv2.rectangle(overlay, (fx - 6, SIZE - 46), (fx + f_sz[0] + 6, SIZE - 26), hud_color, 1)
        cv2.putText(overlay, footer_text, (fx, SIZE - 31), font_mono, 0.85, color_cyan, 1, cv2.LINE_AA)
        
    elif mode == "OP":
        # Header Badge
        header_text = "PUBG // SPEC-OPS L3"
        t_sz = cv2.getTextSize(header_text, font_mono, 0.9, 1)[0]
        tx = CX - t_sz[0] // 2
        cv2.rectangle(overlay, (tx - 6, 26), (tx + t_sz[0] + 6, 46), (15, 25, 20), -1)
        cv2.rectangle(overlay, (tx - 6, 26), (tx + t_sz[0] + 6, 46), hud_color, 1)
        cv2.putText(overlay, header_text, (tx, 41), font_mono, 0.9, color_white, 1, cv2.LINE_AA)
        
        # Reticle Target Brackets near center
        ret_r = 75
        cv2.circle(overlay, (CX, CY), ret_r, hud_color, 1, cv2.LINE_AA)
        # 4 reticle ticks
        cv2.line(overlay, (CX - ret_r - 5, CY), (CX - ret_r + 5, CY), hud_color, 1)
        cv2.line(overlay, (CX + ret_r - 5, CY), (CX + ret_r + 5, CY), hud_color, 1)
        cv2.line(overlay, (CX, CY - ret_r - 5), (CX, CY - ret_r + 5), hud_color, 1)
        cv2.line(overlay, (CX, CY + ret_r - 5), (CX, CY + ret_r + 5), hud_color, 1)
        
        # Footer Badge
        footer_text = "ARMED // POCHINKI"
        f_sz = cv2.getTextSize(footer_text, font_mono, 0.85, 1)[0]
        fx = CX - f_sz[0] // 2
        cv2.rectangle(overlay, (fx - 6, SIZE - 46), (fx + f_sz[0] + 6, SIZE - 26), (15, 25, 20), -1)
        cv2.rectangle(overlay, (fx - 6, SIZE - 46), (fx + f_sz[0] + 6, SIZE - 26), hud_color, 1)
        cv2.putText(overlay, footer_text, (fx, SIZE - 31), font_mono, 0.85, color_emerald, 1, cv2.LINE_AA)
        
    if notice:
        n_sz = cv2.getTextSize(notice, font_mono, 0.95, 1)[0]
        nx = CX - n_sz[0] // 2
        cv2.rectangle(overlay, (nx - 8, CY - 14), (nx + n_sz[0] + 8, CY + 14), (10, 10, 15), -1)
        cv2.rectangle(overlay, (nx - 8, CY - 14), (nx + n_sz[0] + 8, CY + 14), hud_color, 1)
        cv2.putText(overlay, notice, (nx, CY + 6), font_mono, 0.95, color_white, 1, cv2.LINE_AA)
        
    # Mask strictly to circle
    circular_final = np.zeros_like(img)
    circular_final[circle_mask > 0] = overlay[circle_mask > 0]
    return circular_final

print("Generating 120-frame ultra-tactical circular avatar sequence...")

for f in range(TOTAL_FRAMES):
    # 0..39: DEV Mode (1.67s)
    # 40..59: DEV -> OPERATOR Morph (0.83s, 20 frames)
    # 60..99: OPERATOR Mode (1.67s)
    # 100..119: OPERATOR -> DEV Reverse Morph (0.83s, 20 frames)
    
    if 0 <= f < 40:
        scale = 1.0 + 0.005 * math.sin(f * 2 * math.pi / 40)
        M = cv2.getRotationMatrix2D((CX, CY), 0, scale)
        frame = cv2.warpAffine(im_dev, M, (SIZE, SIZE), borderMode=cv2.BORDER_REFLECT)
        frame = draw_tactical_hud(frame, mode="DEV", frame_idx=f)
        
    elif 40 <= f < 60:
        p = (f - 40) / 20.0
        if f in (40, 41):
            frame = apply_chromatic_aberration(im_dev, 10)
            frame = apply_slice_glitch(frame, intensity=1.5)
            frame = draw_tactical_hud(frame, mode="TRANS_DEV", frame_idx=f, notice=">>> TACTICAL OVERRIDE <<<")
        else:
            scan_y = int(p * (SIZE + 40)) - 20
            frame = np.zeros_like(im_dev)
            block_size = 10
            for by in range(0, SIZE, block_size):
                for bx in range(0, SIZE, block_size):
                    dist = by - scan_y
                    if dist < -12:
                        frame[by:by+block_size, bx:bx+block_size] = im_op[by:by+block_size, bx:bx+block_size]
                    elif dist > 12:
                        frame[by:by+block_size, bx:bx+block_size] = im_dev[by:by+block_size, bx:bx+block_size]
                    else:
                        if random.random() < (1.0 - (dist + 12) / 24.0):
                            frame[by:by+block_size, bx:bx+block_size] = im_op[by:by+block_size, bx:bx+block_size]
                        else:
                            frame[by:by+block_size, bx:bx+block_size] = im_dev[by:by+block_size, bx:bx+block_size]
            
            # Holographic wireframe + high-intensity laser
            if 0 <= scan_y < SIZE:
                wireframe = np.zeros_like(frame)
                wireframe[edges_op > 0] = (255, 230, 0) # Cyan wireframe
                y1 = max(0, scan_y - 20)
                y2 = min(SIZE, scan_y + 20)
                frame[y1:y2, :] = cv2.addWeighted(frame[y1:y2, :], 0.7, wireframe[y1:y2, :], 0.6, 0)
                
                cv2.line(frame, (0, scan_y), (SIZE, scan_y), (255, 255, 255), 2)
                cv2.line(frame, (0, scan_y - 1), (SIZE, scan_y - 1), (255, 200, 0), 1)
                cv2.line(frame, (0, scan_y + 1), (SIZE, scan_y + 1), (255, 200, 0), 1)
                
            frame = apply_chromatic_aberration(frame, int(7 * (1.0 - abs(p - 0.5) * 2)))
            if random.random() > 0.4:
                frame = apply_slice_glitch(frame, intensity=0.7)
            frame = draw_tactical_hud(frame, mode="TRANS_OP", frame_idx=f, notice="[DEPLOY: L3 ARMOR]")
            
    elif 60 <= f < 100:
        scale = 1.0 + 0.005 * math.sin((f - 60) * 2 * math.pi / 40)
        M = cv2.getRotationMatrix2D((CX, CY), 0, scale)
        frame = cv2.warpAffine(im_op, M, (SIZE, SIZE), borderMode=cv2.BORDER_REFLECT)
        frame = draw_tactical_hud(frame, mode="OP", frame_idx=f)
        
    else:
        # REVERSE MORPH (100..119)
        p = (f - 100) / 20.0
        if f in (100, 101):
            frame = apply_chromatic_aberration(im_op, 10)
            frame = apply_slice_glitch(frame, intensity=1.5)
            frame = draw_tactical_hud(frame, mode="TRANS_DEV", frame_idx=f, notice=">>> SYSTEM DISENGAGE <<<")
        else:
            scan_y = int((1.0 - p) * (SIZE + 40)) - 20
            frame = np.zeros_like(im_op)
            block_size = 10
            for by in range(0, SIZE, block_size):
                for bx in range(0, SIZE, block_size):
                    dist = by - scan_y
                    if dist > 12:
                        frame[by:by+block_size, bx:bx+block_size] = im_dev[by:by+block_size, bx:bx+block_size]
                    elif dist < -12:
                        frame[by:by+block_size, bx:bx+block_size] = im_op[by:by+block_size, bx:bx+block_size]
                    else:
                        if random.random() < ((dist + 12) / 24.0):
                            frame[by:by+block_size, bx:bx+block_size] = im_dev[by:by+block_size, bx:bx+block_size]
                        else:
                            frame[by:by+block_size, bx:bx+block_size] = im_op[by:by+block_size, bx:bx+block_size]
                            
            if 0 <= scan_y < SIZE:
                wireframe = np.zeros_like(frame)
                wireframe[edges_dev > 0] = (80, 220, 50)
                y1 = max(0, scan_y - 20)
                y2 = min(SIZE, scan_y + 20)
                frame[y1:y2, :] = cv2.addWeighted(frame[y1:y2, :], 0.7, wireframe[y1:y2, :], 0.6, 0)
                
                cv2.line(frame, (0, scan_y), (SIZE, scan_y), (255, 255, 255), 2)
                cv2.line(frame, (0, scan_y - 1), (SIZE, scan_y - 1), (80, 220, 50), 1)
                cv2.line(frame, (0, scan_y + 1), (SIZE, scan_y + 1), (80, 220, 50), 1)
                
            frame = apply_chromatic_aberration(frame, int(7 * (1.0 - abs(p - 0.5) * 2)))
            if random.random() > 0.4:
                frame = apply_slice_glitch(frame, intensity=0.7)
            frame = draw_tactical_hud(frame, mode="TRANS_DEV", frame_idx=f, notice="[RESTORING: DEV_MODE]")

    frame_path = os.path.join(FRAMES_DIR, f"frame_{f:04d}.png")
    cv2.imwrite(frame_path, frame)

print(f"Generated {TOTAL_FRAMES} frames cleanly.")
