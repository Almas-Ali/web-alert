"""Job Log Viewer Dialog."""

from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk


class JobLogViewer(ctk.CTkToplevel):
    """Dialog for viewing and editing job logs."""

    def __init__(self, parent, job, db):
        """Initialize the job log viewer.

        Args:
            parent: Parent window
            job: MonitorJob instance
            db: ConfigDatabase instance
        """
        super().__init__(parent)

        self.job = job
        self.db = db

        self.title(f"Job Logs - {job.url[:50]}")
        self.geometry("900x600")

        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 450
        y = (self.winfo_screenheight() // 2) - 300
        self.geometry(f"900x600+{x}+{y}")

        self.transient(parent)

        self._create_widgets()
        self._load_logs()

    def _create_widgets(self):
        """Create viewer widgets."""
        # Modern header
        header = ctk.CTkFrame(
            self, fg_color=("#6C63FF", "#6C63FF"), corner_radius=0, height=55
        )
        header.pack(fill="x", pady=(0, 10))
        header.pack_propagate(False)

        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(
            header_content,
            text=f"📋 Activity Log",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white",
        ).pack(side="left")

        # Stats badges
        stats_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        stats_frame.pack(side="right")

        ctk.CTkLabel(
            stats_frame,
            text=f"🔄 {self.job.changes_detected}",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="white",
            text_color=("#6C63FF", "#6C63FF"),
            corner_radius=6,
            padx=8,
            pady=3,
        ).pack(side="left", padx=2)

        ctk.CTkLabel(
            stats_frame,
            text=f"🔔 {self.job.alerts_played}",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="white",
            text_color=("#6C63FF", "#6C63FF"),
            corner_radius=6,
            padx=8,
            pady=3,
        ).pack(side="left", padx=2)

        # URL info
        url_frame = ctk.CTkFrame(self)
        url_frame.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(
            url_frame, text=f"🌐 {self.job.url}", font=ctk.CTkFont(size=12), anchor="w"
        ).pack(padx=10, pady=8)

        # Tabs
        tab_view = ctk.CTkTabview(self)
        tab_view.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Activity Log Tab
        log_tab = tab_view.add("Activity Log")

        # Log controls
        control_frame = ctk.CTkFrame(log_tab, fg_color="transparent")
        control_frame.pack(fill="x", pady=(5, 10))

        ctk.CTkButton(
            control_frame, text="🔄 Refresh", command=self._load_logs, width=100
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            control_frame,
            text="🗑️ Clear Logs",
            command=self._clear_logs,
            width=100,
            fg_color="#e74c3c",
            hover_color="#c0392b",
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            control_frame, text="💾 Export", command=self._export_logs, width=100
        ).pack(side="left", padx=5)

        self.auto_refresh_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            control_frame,
            text="Auto-refresh",
            variable=self.auto_refresh_var,
            command=self._toggle_auto_refresh,
        ).pack(side="right", padx=5)

        # Log text area
        self.log_text = ctk.CTkTextbox(log_tab, wrap="word")
        self.log_text.pack(fill="both", expand=True)

        # Notes Tab
        notes_tab = tab_view.add("Notes")

        ctk.CTkLabel(
            notes_tab,
            text="Add your notes about this monitoring job:",
            font=ctk.CTkFont(size=12),
            anchor="w",
        ).pack(fill="x", pady=(10, 5), padx=10)

        self.notes_text = ctk.CTkTextbox(notes_tab, wrap="word")
        self.notes_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.notes_text.insert("1.0", self.job.notes)

        ctk.CTkButton(
            notes_tab,
            text="💾 Save Notes",
            command=self._save_notes,
            fg_color="#2ecc71",
            hover_color="#27ae60",
        ).pack(pady=5)

        # Settings Tab
        settings_tab = tab_view.add("Settings")

        settings_frame = ctk.CTkFrame(settings_tab, fg_color="transparent")
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Display job settings
        settings_info = f"""
Job Configuration:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
URL: {self.job.url}
CSS Selector: {self.job.selector if self.job.selector else "None (Full page)"}
Check Interval: {self.job.check_interval} seconds
Comparison Mode: {self.job.comparison_mode}
Alert Sound: {self.job.alert_sound if self.job.alert_sound else "Default"}
Timeout: {self.job.timeout} seconds
Created: {self.job.created_at.strftime("%Y-%m-%d %H:%M:%S")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: {self.job.status}
Last Check: {self.job.last_check.strftime("%Y-%m-%d %H:%M:%S") if self.job.last_check else "Never"}
Total Changes Detected: {self.job.changes_detected}
Total Alerts Played: {self.job.alerts_played}
Total Log Entries: {len(self.job.logs)}
        """

        ctk.CTkTextbox(settings_frame, wrap="word").pack(fill="both", expand=True)

        settings_text = settings_frame.winfo_children()[0]
        settings_text.insert("1.0", settings_info.strip())
        settings_text.configure(state="disabled")

        # Close button
        ctk.CTkButton(self, text="Close", command=self.destroy, width=120).pack(
            pady=(0, 15)
        )

        # Auto-refresh state
        self.auto_refresh_after_id = None

    def _load_logs(self):
        """Load logs from job."""
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")

        if not self.job.logs:
            self.log_text.insert(
                "1.0", "No logs yet. Logs will appear here when monitoring starts.\n"
            )
        else:
            for log_entry in self.job.logs:
                self.log_text.insert("end", log_entry + "\n")

        self.log_text.see("end")

    def _clear_logs(self):
        """Clear all logs."""
        if messagebox.askyesno("Confirm", "Clear all logs for this job?"):
            self.job.logs.clear()
            self._load_logs()

    def _export_logs(self):
        """Export logs to file."""
        filename = filedialog.asksaveasfilename(
            title="Export Logs",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"job_logs_{self.job.id[:8]}.txt",
        )

        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"Job Logs for: {self.job.url}\n")
                    f.write(
                        f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    )
                    f.write("=" * 80 + "\n\n")
                    f.write(self.log_text.get("1.0", "end"))
                messagebox.showinfo("Success", f"Logs exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export logs: {e}")

    def _save_notes(self):
        """Save notes."""
        self.job.notes = self.notes_text.get("1.0", "end-1c")

        # Save to database
        job_data = self.job.to_dict()
        self.db.save_active_job(job_data)

        messagebox.showinfo("Success", "Notes saved!")

    def _toggle_auto_refresh(self):
        """Toggle auto-refresh."""
        if self.auto_refresh_var.get():
            self._auto_refresh()
        else:
            if self.auto_refresh_after_id:
                self.after_cancel(self.auto_refresh_after_id)

    def _auto_refresh(self):
        """Auto-refresh logs."""
        if self.auto_refresh_var.get():
            self._load_logs()
            self.auto_refresh_after_id = self.after(2000, self._auto_refresh)
