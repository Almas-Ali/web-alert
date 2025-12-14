"""Job management service."""

import logging
import threading
import time
import uuid
from typing import Dict, Optional

from ..core import MonitorJob
from ..data import ConfigDatabase

logger = logging.getLogger(__name__)


class JobManager:
    """Manages monitoring jobs lifecycle."""

    def __init__(self, db: ConfigDatabase):
        """Initialize the job manager.

        Args:
            db: ConfigDatabase instance
        """
        self.db = db
        self.jobs: Dict[str, MonitorJob] = {}

    def create_job(self, config: dict, saved: bool = False) -> tuple[str, MonitorJob]:
        """Create a new monitoring job.

        Args:
            config: Job configuration dictionary
            saved: Whether this is a saved job being loaded

        Returns:
            Tuple of (job_id, job)
        """
        # Use existing ID if loading saved job, otherwise generate new
        job_id = config.get("id", str(uuid.uuid4()))

        job = MonitorJob(
            id=job_id,
            url=config["url"],
            selector=config.get("selector", ""),
            check_interval=config["check_interval"],
            comparison_mode=config["comparison_mode"],
            alert_sound=config.get("alert_sound", ""),
            tts_message=config.get("tts_message", ""),
            timeout=config.get("timeout", 10),
            notes=config.get("notes", ""),
        )

        self.jobs[job_id] = job

        # Save to database if it's a new job (not loading from saved)
        if not saved:
            job_data = job.to_dict()
            job_data["id"] = job_id
            self.db.save_active_job(job_data)

        logger.info(f"Created job {job_id} for {job.url}")
        return job_id, job

    def start_job(self, job_id: str, monitor_callback) -> bool:
        """Start monitoring a specific job.

        Args:
            job_id: ID of the job to start
            monitor_callback: Callback function for monitoring loop

        Returns:
            True if job was started, False otherwise
        """
        if job_id not in self.jobs:
            return False

        job = self.jobs[job_id]

        if job.is_running:
            return False

        job.start()

        # Start monitoring thread
        job.thread = threading.Thread(
            target=monitor_callback, args=(job_id,), daemon=True
        )
        job.thread.start()

        logger.info(f"Started job {job_id}")
        return True

    def stop_job(self, job_id: str, wait: bool = False, timeout: float = 2.0) -> bool:
        """Stop monitoring a specific job.

        Args:
            job_id: ID of the job to stop
            wait: If True, wait for the thread to finish
            timeout: Maximum time to wait for thread to finish

        Returns:
            True if job was stopped, False otherwise
        """
        if job_id not in self.jobs:
            return False

        job = self.jobs[job_id]
        job.stop()
        
        # Wait for thread to finish if requested
        if wait and job.thread and job.thread.is_alive():
            logger.info(f"Waiting for job {job_id} thread to finish...")
            job.thread.join(timeout=timeout)
            if job.thread.is_alive():
                logger.warning(f"Job {job_id} thread did not finish within {timeout}s")

        logger.info(f"Stopped job {job_id}")
        return True

    def remove_job(self, job_id: str) -> bool:
        """Remove a monitoring job.

        Args:
            job_id: ID of the job to remove

        Returns:
            True if job was removed, False otherwise
        """
        if job_id not in self.jobs:
            return False

        job = self.jobs[job_id]

        # Stop if running
        if job.is_running:
            job.stop()

        # Remove from database
        self.db.delete_active_job(job_id)

        # Remove from jobs dict
        del self.jobs[job_id]

        logger.info(f"Removed job {job_id}")
        return True

    def get_job(self, job_id: str) -> Optional[MonitorJob]:
        """Get a job by ID.

        Args:
            job_id: ID of the job

        Returns:
            MonitorJob instance or None if not found
        """
        return self.jobs.get(job_id)

    def get_all_jobs(self) -> Dict[str, MonitorJob]:
        """Get all jobs.

        Returns:
            Dictionary of job_id -> MonitorJob
        """
        return self.jobs

    def start_all_jobs(self, monitor_callback):
        """Start all jobs.

        Args:
            monitor_callback: Callback function for monitoring loop
        """
        for job_id in self.jobs:
            if not self.jobs[job_id].is_running:
                self.start_job(job_id, monitor_callback)

    def stop_all_jobs(self, wait: bool = True, timeout: float = 2.0):
        """Stop all jobs.
        
        Args:
            wait: If True, wait for threads to finish
            timeout: Maximum time to wait per thread
        """
        for job_id in list(self.jobs.keys()):
            if self.jobs[job_id].is_running:
                self.stop_job(job_id, wait=wait, timeout=timeout)

    def load_saved_jobs(self) -> list:
        """Load jobs from database that were active when app closed.

        Returns:
            List of job configurations
        """
        saved_jobs = self.db.get_active_jobs()
        logger.info(f"Loading {len(saved_jobs)} saved jobs")
        return saved_jobs
