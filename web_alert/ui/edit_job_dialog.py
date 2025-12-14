"""Edit Job Dialog."""

from tkinter import filedialog, messagebox

import customtkinter as ctk


class EditJobDialog(ctk.CTkToplevel):
    """Dialog for editing an existing monitoring job."""

    def __init__(self, parent, db, job, callback):
        """Initialize the edit job dialog.

        Args:
            parent: Parent window
            db: ConfigDatabase instance
            job: MonitorJob instance to edit
            callback: Callback function to call when job is updated
        """
        super().__init__(parent)

        self.db = db
        self.job = job
        self.callback = callback
        self.result = None

        self.title("Edit Monitoring Job")
        self.geometry("600x700")

        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 300
        y = (self.winfo_screenheight() // 2) - 350
        self.geometry(f"600x700+{x}+{y}")

        self.transient(parent)
        self.grab_set()

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Modern header
        header = ctk.CTkFrame(self, fg_color=("#8B5CF6", "#8B5CF6"), corner_radius=0)
        header.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            header,
            text="✏️ Edit Monitoring Job",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white",
        ).pack(pady=15, padx=15)

        # Form frame with modern styling
        form_frame = ctk.CTkFrame(self, corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # URL
        ctk.CTkLabel(
            form_frame,
            text="URL *",
            anchor="w",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(fill="x", padx=10, pady=(10, 3))
        self.url_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="https://example.com",
            height=32,
            corner_radius=8,
            border_width=2,
        )
        self.url_entry.insert(0, self.job.url)
        self.url_entry.pack(fill="x", padx=10, pady=(0, 8))

        # CSS Selector
        ctk.CTkLabel(
            form_frame,
            text="CSS Selector (Optional)",
            anchor="w",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(fill="x", padx=10, pady=(0, 3))
        self.selector_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Leave empty for full page",
            height=32,
            corner_radius=8,
            border_width=2,
        )
        self.selector_entry.insert(0, self.job.selector or "")
        self.selector_entry.pack(fill="x", padx=10, pady=(0, 8))

        # Check Interval
        ctk.CTkLabel(
            form_frame,
            text="Check Interval (seconds) *",
            anchor="w",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(fill="x", padx=10, pady=(0, 3))
        self.interval_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="60",
            height=32,
            corner_radius=8,
            border_width=2,
        )
        self.interval_entry.insert(0, str(self.job.check_interval))
        self.interval_entry.pack(fill="x", padx=10, pady=(0, 8))

        # Comparison Mode
        ctk.CTkLabel(
            form_frame,
            text="Comparison Mode",
            anchor="w",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(fill="x", padx=10, pady=(0, 3))
        self.mode_var = ctk.StringVar(value=self.job.comparison_mode)
        mode_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        mode_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkOptionMenu(
            mode_frame, values=["text", "html", "hash"], variable=self.mode_var
        ).pack(side="left")

        # Alert Sound
        ctk.CTkLabel(
            form_frame,
            text="Alert Sound (Optional)",
            anchor="w",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(fill="x", padx=10, pady=(0, 3))
        sound_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        sound_frame.pack(fill="x", padx=10, pady=(0, 8))

        self.sound_entry = ctk.CTkEntry(
            sound_frame,
            placeholder_text="Default system sound",
            height=32,
            corner_radius=8,
            border_width=2,
        )
        self.sound_entry.insert(0, self.job.alert_sound or "")
        self.sound_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ctk.CTkButton(
            sound_frame,
            text="Browse",
            width=80,
            height=32,
            command=self._browse_sound,
            corner_radius=8,
        ).pack(side="left")

        # TTS Message
        ctk.CTkLabel(
            form_frame,
            text="🔊 Text-to-Speech Message (Optional)",
            anchor="w",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(fill="x", padx=10, pady=(0, 3))
        
        tts_info = ctk.CTkLabel(
            form_frame,
            text="💡 This message will be spoken when a change is detected",
            anchor="w",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
        )
        tts_info.pack(fill="x", padx=10, pady=(0, 3))
        
        self.tts_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="e.g., 'Alert! Website has changed'",
            height=32,
            corner_radius=8,
            border_width=2,
        )
        self.tts_entry.insert(0, self.job.tts_message or "")
        self.tts_entry.pack(fill="x", padx=10, pady=(0, 8))

        # Notes
        ctk.CTkLabel(
            form_frame,
            text="Notes (Optional)",
            anchor="w",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(fill="x", padx=10, pady=(0, 3))
        self.notes_entry = ctk.CTkTextbox(
            form_frame,
            height=60,
            corner_radius=8,
            border_width=2,
        )
        self.notes_entry.insert("1.0", self.job.notes or "")
        self.notes_entry.pack(fill="x", padx=10, pady=(0, 8))

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkButton(
            button_frame,
            text="Save Changes",
            command=self._save_changes,
            fg_color="#10B981",
            hover_color="#059669",
            width=150,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=150,
        ).pack(side="right", padx=5)

    def _browse_sound(self):
        """Browse for sound file."""
        filename = filedialog.askopenfilename(
            title="Select Alert Sound",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
        )
        if filename:
            self.sound_entry.delete(0, "end")
            self.sound_entry.insert(0, filename)

    def _save_changes(self):
        """Save the changes and close dialog."""
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showwarning("Missing URL", "Please enter a URL to monitor.")
            return

        if not url.startswith(("http://", "https://")):
            messagebox.showwarning(
                "Invalid URL", "URL must start with http:// or https://"
            )
            return

        try:
            interval = int(self.interval_entry.get())
            if interval < 1:
                raise ValueError("Interval must be at least 1 second")
        except ValueError as e:
            messagebox.showerror("Invalid Interval", str(e))
            return

        config = {
            "url": url,
            "selector": self.selector_entry.get().strip(),
            "check_interval": interval,
            "comparison_mode": self.mode_var.get(),
            "alert_sound": self.sound_entry.get().strip(),
            "tts_message": self.tts_entry.get().strip(),
            "timeout": 10,
        }

        # Update notes
        notes = self.notes_entry.get("1.0", "end-1c").strip()
        self.job.notes = notes

        # Save to database configuration history
        self.db.save_config(config)

        self.callback(self.job.id, config)
        self.destroy()
