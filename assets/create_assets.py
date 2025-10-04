#!/usr/bin/env python3
"""
Script to create all asset files for VocalShell programmatically
"""

import os
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import wave
import struct

def create_directory_structure():
    """Create the assets directory structure"""
    directories = [
        'assets/icons',
        'assets/sounds'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def create_app_icon_ico():
    """Create a simple Windows app icon (.ico)"""
    try:
        # Create a simple microphone icon
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        for size in sizes:
            # Create image with transparent background
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw microphone icon
            width, height = size
            center_x, center_y = width // 2, height // 2
            
            # Microphone body
            body_width = width // 3
            body_height = height // 2
            body_x1 = center_x - body_width // 2
            body_y1 = center_y - body_height // 3
            body_x2 = center_x + body_width // 2
            body_y2 = center_y + body_height // 2
            
            # Draw microphone
            draw.ellipse([body_x1, body_y1, body_x2, body_y2], fill='#2563eb')
            
            # Microphone stand
            stand_width = body_width // 3
            stand_height = height // 4
            stand_x1 = center_x - stand_width // 2
            stand_y1 = body_y2
            stand_x2 = center_x + stand_width // 2
            stand_y2 = stand_y1 + stand_height
            
            draw.rectangle([stand_x1, stand_y1, stand_x2, stand_y2], fill='#2563eb')
            
            # Base
            base_width = body_width
            base_height = height // 8
            base_x1 = center_x - base_width // 2
            base_y1 = stand_y2
            base_x2 = center_x + base_width // 2
            base_y2 = base_y1 + base_height
            
            draw.rectangle([base_x1, base_y1, base_x2, base_y2], fill='#1d4ed8')
            
            # Save as PNG first, then we'll create ICO
            png_path = f"assets/icons/app_icon_{size[0]}x{size[1]}.png"
            img.save(png_path, 'PNG')
            print(f"Created: {png_path}")
        
        print("Note: For a proper .ico file, you might want to use an online converter")
        print("or specialized software to convert these PNGs to ICO format.")
        
    except Exception as e:
        print(f"Error creating app icon: {e}")

def create_microphone_png():
    """Create a microphone PNG icon"""
    try:
        # Create a larger microphone icon for GUI
        size = (512, 512)
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        width, height = size
        center_x, center_y = width // 2, height // 2
        
        # Modern microphone design
        # Main body (circle)
        body_radius = min(width, height) // 3
        draw.ellipse([
            center_x - body_radius,
            center_y - body_radius,
            center_x + body_radius,
            center_y + body_radius
        ], fill='#3b82f6', outline='#1d4ed8', width=5)
        
        # Microphone grille
        grille_radius = body_radius - 20
        for i in range(8):
            angle = i * 45
            rad = np.radians(angle)
            x1 = center_x + grille_radius * 0.7 * np.cos(rad)
            y1 = center_y + grille_radius * 0.7 * np.sin(rad)
            x2 = center_x + grille_radius * np.cos(rad)
            y2 = center_y + grille_radius * np.sin(rad)
            draw.line([x1, y1, x2, y2], fill='#ffffff', width=3)
        
        # Center dot
        dot_radius = 8
        draw.ellipse([
            center_x - dot_radius,
            center_y - dot_radius,
            center_x + dot_radius,
            center_y + dot_radius
        ], fill='#ffffff')
        
        # Stand
        stand_width = body_radius // 2
        stand_height = height // 6
        stand_x1 = center_x - stand_width // 2
        stand_y1 = center_y + body_radius
        stand_x2 = center_x + stand_width // 2
        stand_y2 = stand_y1 + stand_height
        
        draw.rectangle([stand_x1, stand_y1, stand_x2, stand_y2], fill='#1d4ed8')
        
        # Base
        base_width = body_radius
        base_height = height // 12
        base_x1 = center_x - base_width // 2
        base_y1 = stand_y2
        base_x2 = center_x + base_width // 2
        base_y2 = base_y1 + base_height
        
        draw.rounded_rectangle([base_x1, base_y1, base_x2, base_y2], 
                             radius=10, fill='#1e40af')
        
        # Save the image
        img.save('assets/icons/microphone.png', 'PNG')
        print("Created: assets/icons/microphone.png")
        
    except Exception as e:
        print(f"Error creating microphone PNG: {e}")

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    """Generate a sine wave"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave_data

def create_listen_start_wav():
    """Create a gentle start listening sound"""
    try:
        # Create a gentle rising tone
        sample_rate = 44100
        duration = 0.8
        
        # Generate a rising frequency sweep
        t = np.linspace(0, duration, int(sample_rate * duration))
        start_freq = 400
        end_freq = 800
        
        # Linear frequency sweep
        frequencies = np.linspace(start_freq, end_freq, len(t))
        wave_data = 0.3 * np.sin(2 * np.pi * frequencies * t)
        
        # Apply fade in
        fade_samples = int(0.1 * sample_rate)
        fade_in = np.linspace(0, 1, fade_samples)
        wave_data[:fade_samples] *= fade_in
        
        # Apply fade out
        fade_out = np.linspace(1, 0, fade_samples)
        wave_data[-fade_samples:] *= fade_out
        
        # Convert to 16-bit integers
        wave_data_normalized = np.int16(wave_data * 32767)
        
        # Write WAV file
        with wave.open('assets/sounds/listen_start.wav', 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
            wav_file.setframerate(sample_rate)
            wav_file.setcomptype('NONE', 'not compressed')
            
            # Write frames
            for sample in wave_data_normalized:
                data = struct.pack('<h', sample)
                wav_file.writeframesraw(data)
        
        print("Created: assets/sounds/listen_start.wav")
        
    except Exception as e:
        print(f"Error creating listen start sound: {e}")

def create_command_success_wav():
    """Create a success confirmation sound"""
    try:
        sample_rate = 44100
        duration = 0.6
        
        # Create a pleasant success chord (C major)
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # C major chord frequencies (C4, E4, G4)
        freq1 = 261.63  # C4
        freq2 = 329.63  # E4
        freq3 = 392.00  # G4
        
        # Generate chord
        wave1 = 0.2 * np.sin(2 * np.pi * freq1 * t)
        wave2 = 0.2 * np.sin(2 * np.pi * freq2 * t)
        wave3 = 0.2 * np.sin(2 * np.pi * freq3 * t)
        
        wave_data = wave1 + wave2 + wave3
        
        # Apply envelope with quick attack and release
        attack_samples = int(0.05 * sample_rate)
        decay_samples = int(0.4 * sample_rate)
        release_samples = int(0.15 * sample_rate)
        
        # Attack
        attack = np.linspace(0, 1, attack_samples)
        wave_data[:attack_samples] *= attack
        
        # Decay to sustain
        decay = np.linspace(1, 0.7, decay_samples)
        wave_data[attack_samples:attack_samples + decay_samples] *= decay
        
        # Release
        release_start = attack_samples + decay_samples
        release = np.linspace(0.7, 0, release_samples)
        wave_data[release_start:release_start + release_samples] *= release
        
        # Convert to 16-bit integers
        wave_data_normalized = np.int16(wave_data * 32767)
        
        # Write WAV file
        with wave.open('assets/sounds/command_success.wav', 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
            wav_file.setframerate(sample_rate)
            wav_file.setcomptype('NONE', 'not compressed')
            
            # Write frames
            for sample in wave_data_normalized:
                data = struct.pack('<h', sample)
                wav_file.writeframesraw(data)
        
        print("Created: assets/sounds/command_success.wav")
        
    except Exception as e:
        print(f"Error creating command success sound: {e}")

def create_simple_icon_using_text():
    """Create a simple icon using text (fallback method)"""
    try:
        # Create a simple text-based icon
        size = (64, 64)
        img = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Draw microphone symbol using text
        draw.text((20, 10), "🎤", font=font, fill='black')
        
        img.save('assets/icons/microphone_simple.png', 'PNG')
        print("Created: assets/icons/microphone_simple.png")
        
    except Exception as e:
        print(f"Error creating simple icon: {e}")

def create_placeholder_assets():
    """Create placeholder asset files with instructions"""
    
    # Create placeholder icons as text files with instructions
    placeholder_icon = """
This is a placeholder for the application icon.

To create proper icons:

1. For app_icon.ico (Windows):
   - Use a tool like GIMP, Photoshop, or online ICO converter
   - Create icons in multiple sizes: 16x16, 32x32, 48x48, 64x64, 128x128, 256x256
   - Save as .ico format

2. For microphone.png:
   - Create a 512x512 PNG image of a microphone
   - Use transparent background
   - Modern, clean design preferred

You can also run the create_assets.py script to generate basic versions.
"""
    
    with open('assets/icons/PLACEHOLDER_README.txt', 'w') as f:
        f.write(placeholder_icon)
    
    # Create placeholder sounds instructions
    placeholder_sounds = """
Placeholder for audio files.

Required sound files:
- listen_start.wav: Sound played when starting to listen (gentle tone)
- command_success.wav: Sound played when command executes successfully (positive tone)

You can:
1. Use the create_assets.py script to generate basic sounds
2. Record your own sounds
3. Download free sound effects from sites like freesound.org

Format: 44.1kHz, 16-bit, mono WAV files recommended.
"""
    
    with open('assets/sounds/PLACEHOLDER_README.txt', 'w') as f:
        f.write(placeholder_sounds)
    
    print("Created placeholder instructions")

def main():
    """Main function to create all assets"""
    print("Creating VocalShell assets...")
    
    # Create directory structure
    create_directory_structure()
    
    # Create icons
    print("\nCreating icons...")
    create_microphone_png()
    create_simple_icon_using_text()
    
    # Create sounds
    print("\nCreating sounds...")
    create_listen_start_wav()
    create_command_success_wav()
    
    # Create placeholders with instructions
    create_placeholder_assets()
    
    print("\n" + "="*50)
    print("Asset creation completed!")
    print("="*50)
    print("\nGenerated files:")
    print("✅ assets/icons/microphone.png")
    print("✅ assets/icons/microphone_simple.png") 
    print("✅ assets/sounds/listen_start.wav")
    print("✅ assets/sounds/command_success.wav")
    print("✅ assets/icons/PLACEHOLDER_README.txt")
    print("✅ assets/sounds/PLACEHOLDER_README.txt")
    
    print("\nNote: For app_icon.ico, you'll need to:")
    print("1. Convert microphone.png to .ico format using online tools")
    print("2. Or use specialized icon creation software")
    print("3. Save as assets/icons/app_icon.ico")

if __name__ == "__main__":
    main()