"""Add Job Dialog."""

from tkinter import filedialog, messagebox

import customtkinter as ctk


class AddJobDialog(ctk.CTkToplevel):
    """Dialog for adding a new monitoring job."""

    def __init__(self, parent, db, callback):
        """Initialize the add job dialog.

        Args:
            parent: Parent window
            db: ConfigDatabase instance
            callback: Callback function to call when job is added
        """
        super().__init__(parent)

        self.db = db
        self.callback = callback
        self.result = None

        self.title("Add New Monitoring Job")
        self.geometry("600x600")

        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 300
        y = (self.winfo_screenheight() // 2) - 300
        self.geometry(f"600x600+{x}+{y}")

        self.transient(parent)
        self.grab_set()

        self._create_widgets()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Modern header
        header = ctk.CTkFrame(self, fg_color=("#6C63FF", "#6C63FF"), corner_radius=0)
        header.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            header,
            text="➕ Add New Monitoring Job",
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
        self.interval_entry.insert(0, "60")
        self.interval_entry.pack(fill="x", padx=10, pady=(0, 8))

        # Comparison Mode
        ctk.CTkLabel(form_frame, text="Comparison Mode", anchor="w").pack(
            fill="x", padx=10
        )
        self.mode_var = ctk.StringVar(value="text")
        mode_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        mode_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkOptionMenu(
            mode_frame, values=["text", "html", "hash"], variable=self.mode_var
        ).pack(side="left")

        # Alert Sound
        ctk.CTkLabel(form_frame, text="Alert Sound (Optional)", anchor="w").pack(
            fill="x", padx=10
        )
        sound_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        sound_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.sound_entry = ctk.CTkEntry(
            sound_frame, placeholder_text="Default system sound"
        )
        self.sound_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ctk.CTkButton(
            sound_frame, text="Browse", width=80, command=self._browse_sound
        ).pack(side="left")

        # Load from history button
        ctk.CTkButton(
            form_frame,
            text="📜 Load from History",
            command=self._load_from_history,
            fg_color="#3498db",
            hover_color="#2980b9",
        ).pack(pady=10)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkButton(
            button_frame,
            text="Add Job",
            command=self._add_job,
            fg_color="#2ecc71",
            hover_color="#27ae60",
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

    def _load_from_history(self):
        """Load configuration from history."""
        configs = self.db.get_recent_configs(20)

        if not configs:
            messagebox.showinfo("No History", "No configurations found in history.")
            return

        # Create selection window
        select_window = ctk.CTkToplevel(self)
        select_window.title("Select from History")
        select_window.geometry("600x400")
        select_window.transient(self)
        select_window.grab_set()

        ctk.CTkLabel(
            select_window,
            text="Select Configuration",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)

        scrollable = ctk.CTkScrollableFrame(select_window)
        scrollable.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for config in configs:
            frame = ctk.CTkFrame(scrollable)
            frame.pack(fill="x", pady=5, padx=5)

            url_text = (
                config["url"][:50] + "..." if len(config["url"]) > 50 else config["url"]
            )
            ctk.CTkLabel(frame, text=url_text, anchor="w").pack(
                side="left", fill="x", expand=True, padx=10
            )

            ctk.CTkButton(
                frame,
                text="Load",
                width=80,
                command=lambda c=config: self._apply_config(c, select_window),
            ).pack(side="right", padx=10, pady=5)

    def _apply_config(self, config, window):
        """Apply selected configuration."""
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, config["url"])

        self.selector_entry.delete(0, "end")
        self.selector_entry.insert(0, config.get("selector", ""))

        self.interval_entry.delete(0, "end")
        self.interval_entry.insert(0, str(config["check_interval"]))

        self.mode_var.set(config["comparison_mode"])

        if config.get("alert_sound"):
            self.sound_entry.delete(0, "end")
            self.sound_entry.insert(0, config["alert_sound"])

        window.destroy()

    def _add_job(self):
        """Add the job and close dialog."""
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

        self.result = {
            "url": url,
            "selector": self.selector_entry.get().strip(),
            "check_interval": interval,
            "comparison_mode": self.mode_var.get(),
            "alert_sound": self.sound_entry.get().strip(),
            "timeout": 10,
        }

        # Save to database
        self.db.save_config(self.result)

        self.callback(self.result)
        self.destroy()
