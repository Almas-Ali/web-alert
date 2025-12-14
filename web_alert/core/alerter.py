"""Alert system module for playing sound notifications."""

import logging
import os
import sys
import threading
import winsound  # Windows built-in sound support
from pathlib import Path
from typing import Optional

import pyttsx3

# Import pythoncom for Windows COM initialization
if sys.platform == 'win32':
    try:
        import pythoncom
        PYTHONCOM_AVAILABLE = True
    except ImportError:
        PYTHONCOM_AVAILABLE = False
else:
    PYTHONCOM_AVAILABLE = False

logger = logging.getLogger(__name__)

# Global lock for TTS to prevent concurrent speech
_tts_lock = threading.Lock()


class Alerter:
    """Handles alert notifications with sound and text-to-speech."""

    def __init__(self, sound_file: Optional[str] = None, tts_text: Optional[str] = None):
        """
        Initialize the alerter.

        Args:
            sound_file: Path to the sound file to play
            tts_text: Text to speak using text-to-speech
        """
        self.sound_file = sound_file or self._get_default_sound()
        self._validate_sound_file()
        self.alert_count = 0
        
        # Clean up tts_text - convert empty strings, 'None' string, or None to actual None
        if tts_text and tts_text.strip() and tts_text.lower() != 'none':
            self.tts_text = tts_text.strip()
            logger.info(f"Alerter initialized with TTS message: '{self.tts_text}'")
        else:
            self.tts_text = None
            logger.info("Alerter initialized without TTS message")

    def _get_default_sound(self) -> str:
        """Get the default sound file path."""
        base_dir = Path(__file__).parent.parent
        return str(base_dir / "sounds" / "alert.wav")

    def _validate_sound_file(self):
        """Validate that the sound file exists."""
        if not os.path.exists(self.sound_file):
            logger.warning(f"Sound file not found: {self.sound_file}")
            logger.info("Will use system default sound")
            self.sound_file = None

    def play_alert(self, async_play: bool = True):
        """
        Play the alert sound and/or speak the TTS text.

        Args:
            async_play: If True, play sound in background thread
        """
        self.alert_count += 1
        logger.info(f"Playing alert #{self.alert_count}")
        logger.info(f"TTS text configured: '{self.tts_text}'")
        logger.info(f"TTS will {'be' if self.tts_text else 'NOT be'} spoken")

        if async_play:
            # Play in background to not block the main thread
            thread = threading.Thread(target=self._play_alert_complete, daemon=True)
            thread.start()
        else:
            self._play_alert_complete()
    
    def _play_alert_complete(self):
        """Play sound OR speak TTS (mutually exclusive)."""
        # If TTS is configured, only speak (no sound)
        if self.tts_text:
            self._speak_text()
        # Otherwise, play the sound
        else:
            self._play_sound()

    def _play_sound(self):
        """Internal method to play the sound."""
        try:
            if self.sound_file and os.path.exists(self.sound_file):
                # Play custom sound file
                winsound.PlaySound(self.sound_file, winsound.SND_FILENAME)
            else:
                # Play system default sound
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

        except Exception as e:
            logger.error(f"Error playing sound: {e}")
            # Fallback to system beep
            try:
                winsound.Beep(1000, 500)  # 1000Hz for 500ms
            except:
                logger.error("Could not play any sound")

    def test_alert(self):
        """Test the alert sound."""
        logger.info("Testing alert sound...")
        self.play_alert(async_play=False)

    def _speak_text(self):
        """Internal method to speak the TTS text."""
        if not self.tts_text:
            return
        
        # Use lock to prevent concurrent TTS operations
        with _tts_lock:
            try:
                logger.info(f"Speaking TTS: {self.tts_text}")
                
                # Initialize COM for Windows threads
                if PYTHONCOM_AVAILABLE:
                    pythoncom.CoInitialize()
                
                try:
                    # Initialize engine fresh for each speech (better for threading)
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 150)
                    engine.setProperty('volume', 1.0)
                    
                    engine.say(self.tts_text)
                    engine.runAndWait()
                    
                    # Clean up
                    engine.stop()
                    
                    logger.info("TTS completed successfully")
                    
                finally:
                    # Uninitialize COM
                    if PYTHONCOM_AVAILABLE:
                        pythoncom.CoUninitialize()
                
            except Exception as e:
                logger.error(f"Error speaking TTS: {e}", exc_info=True)
    
    def set_sound_file(self, sound_file: str):
        """
        Change the alert sound file.

        Args:
            sound_file: New sound file path
        """
        self.sound_file = sound_file
        self._validate_sound_file()
        logger.info(f"Alert sound changed to: {sound_file}")
    
    def set_tts_text(self, tts_text: str):
        """
        Set or change the TTS text.

        Args:
            tts_text: Text to speak
        """
        self.tts_text = tts_text
        logger.info(f"TTS text changed to: '{tts_text}'")

    def get_alert_count(self) -> int:
        """Get the total number of alerts played."""
        return self.alert_count

    def reset_count(self):
        """Reset the alert counter."""
        self.alert_count = 0
