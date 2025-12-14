"""Streamlined dashboard using modular components."""

import logging
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

from ..config import ConfigManager
from ..core import MonitorJob
from ..data import ConfigDatabase
from ..services import HistoryManager, JobManager, ThemeManager
from ..utils import center_window, setup_logging
from .add_job_dialog import AddJobDialog
from .job_log_viewer import JobLogViewer

logger = setup_logging()


class WebAlertDashboard:
    """Dashboard GUI for managing multiple monitoring jobs."""

    def __init__(self):
        """Initialize the dashboard application."""
        # Initialize backend components
        self.db = ConfigDatabase()
        self.config_manager = ConfigManager(self.db)

        # Initialize services
        self.job_manager = JobManager(self.db)
        self.theme_manager = ThemeManager(self.config_manager)
        self.history_manager = HistoryManager(self.db)

        # Setup GUI
        self._setup_window()
        self.theme_manager.load_theme()
        self.colors = self.theme_manager.get_colors()
        self._create_menu_bar()
        self._create_widgets()

    def _setup_window(self):
        """Setup the main window."""
        self.root = ctk.CTk()
        self.root.title("Web Alert")
        self.root.geometry("700x700")
        self.root.resizable(True, True)

        # Center window
        center_window(self.root, 700, 700)

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_menu_bar(self):
        """Create the menu bar."""
        menu_colors = self.theme_manager.get_menu_colors()

        menubar = tk.Menu(
            self.root,
            bg=menu_colors["bg"],
            fg=menu_colors["fg"],
            activebackground=menu_colors["active_bg"],
            activeforeground=menu_colors["active_fg"],
            borderwidth=0,
            relief="flat",
        )
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=menu_colors["bg"],
            fg=menu_colors["fg"],
            activebackground=menu_colors["active_bg"],
            activeforeground=menu_colors["active_fg"],
            borderwidth=0,
            relief="flat",
        )
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add New Job", command=self._add_job_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Start All Jobs", command=self._start_all_jobs)
        file_menu.add_command(label="Stop All Jobs", command=self._stop_all_jobs)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing)

        # View menu
        view_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=menu_colors["bg"],
            fg=menu_colors["fg"],
            activebackground=menu_colors["active_bg"],
            activeforeground=menu_colors["active_fg"],
            borderwidth=0,
            relief="flat",
        )
        menubar.add_cascade(label="View", menu=view_menu)

        # Theme submenu
        theme_menu = tk.Menu(
            view_menu,
            tearoff=0,
            bg=menu_colors["bg"],
            fg=menu_colors["fg"],
            activebackground=menu_colors["active_bg"],
            activeforeground=menu_colors["active_fg"],
            borderwidth=0,
            relief="flat",
        )
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(
            label="☀️ Light", command=lambda: self._change_theme("light")
        )
        theme_menu.add_command(
            label="🌙 Dark", command=lambda: self._change_theme("dark")
        )
        theme_menu.add_command(
            label="💻 System", command=lambda: self._change_theme("system")
        )

        # History menu
        history_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=menu_colors["bg"],
            fg=menu_colors["fg"],
            activebackground=menu_colors["active_bg"],
            activeforeground=menu_colors["active_fg"],
            borderwidth=0,
            relief="flat",
        )
        menubar.add_cascade(label="History", menu=history_menu)
        history_menu.add_command(label="View All History", command=self._show_history)
        history_menu.add_separator()
        history_menu.add_command(
            label="Clear All History", command=self._clear_all_history
        )
        history_menu.add_command(
            label="Clear Old (Keep 20)", command=self._cleanup_history
        )

        # Help menu
        help_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=menu_colors["bg"],
            fg=menu_colors["fg"],
            activebackground=menu_colors["active_bg"],
            activeforeground=menu_colors["active_fg"],
            borderwidth=0,
            relief="flat",
        )
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)

    def _create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Modern Header
        header_frame = ctk.CTkFrame(
            main_frame, fg_color="#7C3AED", corner_radius=0, height=60
        )
        header_frame.pack(fill="x", pady=(0, 10), padx=0)
        header_frame.pack_propagate(False)

        # Header content
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(
            header_content,
            text="🔔 Web Alert",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white",
        ).pack(side="left", pady=0)

        # Button group
        button_container = ctk.CTkFrame(header_content, fg_color="transparent")
        button_container.pack(side="right")

        ctk.CTkButton(
            button_container,
            text="➕ Add",
            command=self._add_job_dialog,
            width=80,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("white", "white"),
            text_color=("#7C3AED", "#7C3AED"),
            hover_color=("gray90", "gray95"),
            corner_radius=8,
        ).pack(side="right", padx=3)

        ctk.CTkButton(
            button_container,
            text="⏸ Stop",
            command=self._stop_all_jobs,
            width=70,
            height=32,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=("white", "#DC2626"),
            text_color=("#DC2626", "white"),
            hover_color=("gray90", "#B91C1C"),
            corner_radius=8,
            border_width=2,
            border_color=("#DC2626", "#DC2626"),
        ).pack(side="right", padx=3)

        ctk.CTkButton(
            button_container,
            text="▶ Start",
            command=self._start_all_jobs,
            width=70,
            height=32,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=("white", "#10B981"),
            text_color=("#10B981", "white"),
            hover_color=("gray90", "#059669"),
            corner_radius=8,
            border_width=2,
            border_color=("#10B981", "#10B981"),
        ).pack(side="right", padx=3)

        # Jobs container
        jobs_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        jobs_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # Section title
        ctk.CTkLabel(
            jobs_container,
            text="Monitoring Jobs",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 8))

        self.jobs_frame = ctk.CTkScrollableFrame(
            jobs_container,
            fg_color="transparent",
            corner_radius=15,
            scrollbar_fg_color=("gray92", "#0F172A"),
            scrollbar_button_color=("gray92", "#0F172A"),
            scrollbar_button_hover_color=("gray88", "#1E293B"),
        )
        self.jobs_frame.pack(fill="both", expand=True)

        # Empty state
        empty_container = ctk.CTkFrame(
            self.jobs_frame,
            fg_color=self.colors["card_bg"],
            corner_radius=15,
            border_width=1,
            border_color=self.colors["border"],
        )
        empty_container.pack(pady=20, padx=10)

        self.empty_label = ctk.CTkLabel(
            empty_container,
            text="📭 No monitoring jobs yet\n\nClick 'Add' to start monitoring websites!",
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray70"),
            justify="center",
        )
        self.empty_label.pack(padx=40, pady=30)

        # Load saved jobs
        self._load_saved_jobs()

    def _load_saved_jobs(self):
        """Load jobs from database."""
        saved_jobs = self.job_manager.load_saved_jobs()

        if saved_jobs:
            # Hide empty label when loading saved jobs
            if self.empty_label.winfo_viewable():
                self.empty_label.pack_forget()

            for job_data in saved_jobs:
                job_id, job = self.job_manager.create_job(job_data, saved=True)
                self._create_job_widget(job)

    def _add_job_dialog(self):
        """Show dialog to add new job."""
        AddJobDialog(self.root, self.db, self._create_job_from_dialog)

    def _create_job_from_dialog(self, config: dict):
        """Create a job from dialog configuration."""
        job_id, job = self.job_manager.create_job(config)
        self._create_job_widget(job)

        # Hide empty label if visible
        if self.empty_label.winfo_viewable():
            self.empty_label.pack_forget()

    def _create_job_widget(self, job: MonitorJob):
        """Create widget for a monitoring job."""
        job_frame = ctk.CTkFrame(
            self.jobs_frame,
            fg_color=self.colors["card_bg"],
            corner_radius=10,
            border_width=1,
            border_color=self.colors["border"],
        )
        job_frame.pack(fill="x", padx=3, pady=3)

        # Store reference
        job.widget = job_frame

        # Info frame
        info_frame = ctk.CTkFrame(job_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # URL
        url_container = ctk.CTkFrame(info_frame, fg_color="transparent")
        url_container.pack(fill="x", pady=(0, 4))

        url_text = job.url[:80] + "..." if len(job.url) > 80 else job.url
        url_label = ctk.CTkLabel(
            url_container,
            text=f"🌐 {url_text}",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        url_label.pack(side="left", fill="x", expand=True)
        job.url_label = url_label

        # Details with badges
        details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        details_frame.pack(fill="x", pady=(0, 4))

        # Interval badge
        ctk.CTkLabel(
            details_frame,
            text=f"⏱ {job.check_interval}s",
            font=ctk.CTkFont(size=10),
            fg_color=("#3B82F6", "#3B82F6"),
            text_color="white",
            corner_radius=6,
            padx=6,
            pady=2,
        ).pack(side="left", padx=(0, 3))

        # Mode badge
        ctk.CTkLabel(
            details_frame,
            text=f"🔍 {job.comparison_mode}",
            font=ctk.CTkFont(size=10),
            fg_color=("#8B5CF6", "#8B5CF6"),
            text_color="white",
            corner_radius=6,
            padx=6,
            pady=2,
        ).pack(side="left", padx=(0, 3))

        if job.selector:
            selector_text = (
                job.selector[:20] + "..." if len(job.selector) > 20 else job.selector
            )
            ctk.CTkLabel(
                details_frame,
                text=f"📌 {selector_text}",
                font=ctk.CTkFont(size=10),
                fg_color=("#64748B", "#475569"),
                text_color="white",
                corner_radius=6,
                padx=6,
                pady=2,
            ).pack(side="left")

        # Status
        status_label = ctk.CTkLabel(
            info_frame,
            text=f"📊 {job.status} • {job.changes_detected} changes • {job.alerts_played} alerts",
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w",
            text_color=job.status_color,
        )
        status_label.pack(fill="x")
        job.status_label = status_label

        # Controls
        control_frame = ctk.CTkFrame(job_frame, fg_color="transparent")
        control_frame.pack(side="right", padx=8, pady=8)

        start_btn = ctk.CTkButton(
            control_frame,
            text="▶ Start",
            command=lambda: self._start_job(job.id),
            width=80,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=self.colors["success"],
            hover_color=self.colors["hover_success"],
            corner_radius=8,
        )
        start_btn.pack(pady=2)
        job.start_button = start_btn

        stop_btn = ctk.CTkButton(
            control_frame,
            text="⏸ Stop",
            command=lambda: self._stop_job(job.id),
            width=80,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=self.colors["danger"],
            hover_color=self.colors["hover_danger"],
            corner_radius=8,
            state="disabled",
        )
        stop_btn.pack(pady=2)
        job.stop_button = stop_btn

        ctk.CTkButton(
            control_frame,
            text="📋 Logs",
            command=lambda: self._view_job_logs(job.id),
            width=80,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=self.colors["info"],
            hover_color=self.colors["hover_info"],
            corner_radius=8,
        ).pack(pady=2)

        ctk.CTkButton(
            control_frame,
            text="🗑 Remove",
            command=lambda: self._remove_job(job.id),
            width=80,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color=("gray75", "gray30"),
            hover_color=("gray65", "gray35"),
            corner_radius=8,
        ).pack(pady=2)

    def _start_job(self, job_id: str):
        """Start monitoring a specific job."""
        job = self.job_manager.get_job(job_id)
        if not job:
            return

        self.job_manager.start_job(job_id, self._monitor_job)
        job.start_button.configure(state="disabled")
        job.stop_button.configure(state="normal")
        self._update_job_status(job_id)

    def _stop_job(self, job_id: str):
        """Stop monitoring a specific job."""
        job = self.job_manager.get_job(job_id)
        if not job:
            return

        self.job_manager.stop_job(job_id)
        job.start_button.configure(state="normal")
        job.stop_button.configure(state="disabled")
        self._update_job_status(job_id)

    def _remove_job(self, job_id: str):
        """Remove a monitoring job."""
        job = self.job_manager.get_job(job_id)
        if not job:
            return

        if job.is_running:
            if not messagebox.askyesno(
                "Job Running", "This job is currently running. Stop and remove it?"
            ):
                return

        # Remove widget
        job.widget.destroy()

        # Remove job
        self.job_manager.remove_job(job_id)

        # Show empty label if no jobs
        if not self.job_manager.get_all_jobs():
            self.empty_label.pack(pady=50)

    def _view_job_logs(self, job_id: str):
        """View logs for a specific job."""
        job = self.job_manager.get_job(job_id)
        if job:
            JobLogViewer(self.root, job, self.db)

    def _monitor_job(self, job_id: str):
        """Monitor loop for a specific job."""
        job = self.job_manager.get_job(job_id)
        if not job:
            return

        job.add_log("Monitoring started")

        while job.is_running:
            try:
                job.add_log(f"Checking URL: {job.url}")
                content = job.scraper.fetch_content(
                    job.url, job.selector if job.selector else None
                )

                if content is not None:
                    changed = job.detector.detect_change(content)

                    if changed:
                        job.alerter.play_alert()
                        job.update_stats(True, "⚠️ CHANGE DETECTED! Alert triggered")
                        logger.info(f"Change detected for job {job_id}")
                    else:
                        job.update_stats(False, "✓ No changes detected")

                    self.root.after(0, lambda: self._update_job_status(job_id))
                else:
                    job.add_log("❌ Failed to fetch content")

                # Wait for next check
                for i in range(job.check_interval):
                    if not job.is_running:
                        break
                    if i == 0:
                        job.add_log(f"Next check in {job.check_interval} seconds...")
                    time.sleep(1)

            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                job.add_log(error_msg)
                logger.error(f"Error in monitor loop for job {job_id}: {e}")
                time.sleep(5)

        job.add_log("Monitoring stopped")

    def _update_job_status(self, job_id: str):
        """Update job status display."""
        job = self.job_manager.get_job(job_id)
        if not job:
            return

        last_check_str = (
            job.last_check.strftime("%H:%M:%S") if job.last_check else "Never"
        )
        status_text = f"Status: {job.status} | Last Check: {last_check_str} | Changes: {job.changes_detected} | Alerts: {job.alerts_played}"

        job.status_label.configure(text=status_text, text_color=job.status_color)

    def _start_all_jobs(self):
        """Start all jobs."""
        for job_id in self.job_manager.get_all_jobs():
            job = self.job_manager.get_job(job_id)
            if job and not job.is_running:
                self._start_job(job_id)

    def _stop_all_jobs(self):
        """Stop all jobs."""
        for job_id in list(self.job_manager.get_all_jobs().keys()):
            job = self.job_manager.get_job(job_id)
            if job and job.is_running:
                self._stop_job(job_id)

    def _show_history(self):
        """Show configuration history."""
        configs = self.history_manager.get_recent_configs(50)

        if not configs:
            messagebox.showinfo("No History", "No configurations found in history.")
            return

        history_window = ctk.CTkToplevel(self.root)
        history_window.title("Configuration History")
        history_window.geometry("800x500")

        # Center window and set as transient
        history_window.transient(self.root)
        history_window.update_idletasks()
        x = (history_window.winfo_screenwidth() // 2) - 400
        y = (history_window.winfo_screenheight() // 2) - 250
        history_window.geometry(f"800x500+{x}+{y}")

        ctk.CTkLabel(
            history_window,
            text="📜 Configuration History",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=15)

        scrollable = ctk.CTkScrollableFrame(history_window)
        scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        for config in configs:
            frame = ctk.CTkFrame(scrollable)
            frame.pack(fill="x", pady=5, padx=5)

            info_frame = ctk.CTkFrame(frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            url_text = (
                config["url"][:60] + "..." if len(config["url"]) > 60 else config["url"]
            )
            ctk.CTkLabel(
                info_frame,
                text=f"🌐 {url_text}",
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
            ).pack(fill="x")

            details = f"Interval: {config['check_interval']}s | Mode: {config['comparison_mode']} | Uses: {config['use_count']}"
            ctk.CTkLabel(
                info_frame,
                text=details,
                font=ctk.CTkFont(size=10),
                anchor="w",
                text_color="gray",
            ).pack(fill="x")

            ctk.CTkButton(
                frame,
                text="Add as Job",
                width=100,
                command=lambda c=config: self._add_job_from_history(c, history_window),
            ).pack(side="right", padx=10)

        ctk.CTkButton(
            history_window, text="Close", command=history_window.destroy
        ).pack(pady=15)

    def _add_job_from_history(self, config, window):
        """Add a job from history configuration."""
        self._create_job_from_dialog(config)
        window.destroy()
        messagebox.showinfo("Success", "Job added from history!")

    def _cleanup_history(self):
        """Clean up old configurations."""
        if messagebox.askyesno(
            "Confirm Cleanup",
            "Keep only the 20 most recent configurations?\nOlder configurations will be permanently deleted.",
        ):
            self.history_manager.cleanup_old_configs(20)
            messagebox.showinfo("Success", "Old configurations cleaned up!")

    def _clear_all_history(self):
        """Clear all configuration history."""
        if messagebox.askyesno(
            "Confirm Clear All",
            "Delete ALL configuration history?\nThis cannot be undone!",
        ):
            deleted = self.history_manager.clear_all_history()
            messagebox.showinfo(
                "Success", f"Deleted {deleted} configuration(s) from history!"
            )

    def _show_about(self):
        """Show about dialog."""
        about_text = """
Web Alert v2.0.0

A modern web monitoring application that monitors
multiple websites simultaneously and alerts you
when changes are detected.

Features:
• Multiple URL monitoring
• Parallel checking
• Smart change detection
• Configurable monitoring settings
• SQLAlchemy ORM database
• Dashboard interface

Created by Md. Almas Ali
Copyright © 2025. All rights reserved.
        """
        messagebox.showinfo("About Web Alert", about_text.strip())

    def _change_theme(self, theme: str):
        """Change the application theme."""
        try:
            self.theme_manager.change_theme(theme, self._create_menu_bar)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change theme: {str(e)}")

    def _on_closing(self):
        """Handle window close event."""
        jobs = self.job_manager.get_all_jobs()
        running_jobs = [j for j in jobs.values() if j.is_running]

        if running_jobs:
            if messagebox.askokcancel(
                "Quit", f"{len(running_jobs)} job(s) are running. Stop all and quit?"
            ):
                self.job_manager.stop_all_jobs()
                time.sleep(0.5)
                self.root.destroy()
        else:
            self.root.destroy()

    def run(self):
        """Run the application."""
        logger.info("Web Alert started")
        self.root.mainloop()


def main():
    """Main entry point."""
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    app = WebAlertDashboard()
    app.run()


if __name__ == "__main__":
    main()
