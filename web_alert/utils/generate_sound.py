"""Generate a simple alert sound using wave module."""

import math
import struct
import wave


def generate_alert_sound(filename: str, duration: float = 0.5, frequency: int = 1000):
    """
    Generate a simple beep sound as WAV file.

    Args:
        filename: Output filename
        duration: Duration in seconds
        frequency: Frequency in Hz
    """
    sample_rate = 44100
    num_samples = int(sample_rate * duration)

    # Open wave file
    wav_file = wave.open(filename, "w")
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample
    wav_file.setframerate(sample_rate)

    # Generate samples
    for i in range(num_samples):
        # Generate sine wave
        value = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))

        # Add envelope (fade in/out)
        envelope = 1.0
        fade_samples = int(sample_rate * 0.05)  # 50ms fade

        if i < fade_samples:
            envelope = i / fade_samples
        elif i > num_samples - fade_samples:
            envelope = (num_samples - i) / fade_samples

        value = int(value * envelope)

        # Write sample
        data = struct.pack("<h", value)
        wav_file.writeframes(data)

    wav_file.close()


if __name__ == "__main__":
    import os
    from pathlib import Path

    # Create sounds directory if it doesn't exist
    sounds_dir = Path(__file__).parent.parent / "sounds"
    sounds_dir.mkdir(exist_ok=True)

    # Generate alert sound
    output_file = sounds_dir / "alert.wav"
    generate_alert_sound(str(output_file), duration=0.5, frequency=1000)
    print(f"Alert sound generated: {output_file}")
