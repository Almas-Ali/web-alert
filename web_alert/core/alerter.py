"""Alert system module for playing sound notifications."""

import logging
import os
import threading
import winsound  # Windows built-in sound support
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class Alerter:
    """Handles alert notifications with sound."""

    def __init__(self, sound_file: Optional[str] = None):
        """
        Initialize the alerter.

        Args:
            sound_file: Path to the sound file to play
        """
        self.sound_file = sound_file or self._get_default_sound()
        self._validate_sound_file()
        self.alert_count = 0

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
        Play the alert sound.

        Args:
            async_play: If True, play sound in background thread
        """
        self.alert_count += 1
        logger.info(f"Playing alert #{self.alert_count}")

        if async_play:
            # Play in background to not block the main thread
            thread = threading.Thread(target=self._play_sound, daemon=True)
            thread.start()
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

    def set_sound_file(self, sound_file: str):
        """
        Change the alert sound file.

        Args:
            sound_file: New sound file path
        """
        self.sound_file = sound_file
        self._validate_sound_file()
        logger.info(f"Alert sound changed to: {sound_file}")

    def get_alert_count(self) -> int:
        """Get the total number of alerts played."""
        return self.alert_count

    def reset_count(self):
        """Reset the alert counter."""
        self.alert_count = 0
