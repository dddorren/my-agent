import schedule
import time
from datetime import datetime
from typing import Callable
import logging
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)

class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False
    
    def add_daily_task(self, func: Callable, hour: int = 9, minute: int = 0):
        self.scheduler.add_job(
            func,
            'cron',
            hour=hour,
            minute=minute,
            id=f"daily_task_{hour}_{minute}"
        )
        logger.info(f"Added daily task at {hour}:{minute}")
    
    def add_hourly_task(self, func: Callable, minute: int = 0):
        self.scheduler.add_job(
            func,
            'cron',
            minute=minute,
            id=f"hourly_task_{minute}"
        )
        logger.info(f"Added hourly task at minute {minute}")
    
    def add_interval_task(self, func: Callable, minutes: int = 60):
        self.scheduler.add_job(
            func,
            'interval',
            minutes=minutes,
            id=f"interval_task_{minutes}"
        )
        logger.info(f"Added interval task every {minutes} minutes")
    
    def start(self):
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduler started")
    
    def stop(self):
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler stopped")
    
    def run_now(self, func: Callable):
        logger.info(f"Running task immediately: {func.__name__}")
        func()
    
    def get_jobs(self):
        return self.scheduler.get_jobs()
