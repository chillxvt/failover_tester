from concurrent.futures import ThreadPoolExecutor, as_completed
from tester.core.logger import logga
from ping3 import ping
import threading
from datetime import datetime

class Tester:

    def __init__(self, root):
        self.root = root  # Tkinter root to use for after()
        self.logger = logga

        self.armed = False
        self.recording = False
        self.t0 = None
        self.t1 = None

        self.check_interval = 1000  # Interval in milliseconds (e.g., 2 seconds)
        self.targets = []


    def arm(self):
        if len(self.targets) == 0:
            self.logger.warning("No targets specified")
            raise Exception("No targets specified")

        if not self.reachable(self.targets):
            self.logger.warning("No targets reachable, cannot arm")
            raise Exception("No targets reachable, cannot arm")

        self.armed = True
        self.logger.info("Armed. Time recording will start when network becomes unreachable.")
        self.run()

    def disarm(self):
        if self.get_recording():
            self.stop_recording()
        self.armed = False
        self.logger.info("System disarmed.")

    def add_target(self, target_ip):
        if target_ip not in self.targets:
            self.targets.append(target_ip)
            self.logger.info(f'Target {target_ip} added.')
        else:
            raise Exception('Target ip already exists')

    def flush_targets(self, new_targets):
        if not self.reachable(new_targets):
            raise Exception("Some of the targets specified are not reachable")
        self.targets = new_targets

    # Function to ping a single target
    def reachable(self, targets, timeout = 0.5):
        result = True
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.ping_target, target, timeout): target for target in targets}

            for future in as_completed(futures):
                success = future.result()
                if not success:
                    result = False  # Mark as False if any target is unreachable

        return result

    def ping_target(self, target, timeout):
        response_time = ping(target, timeout=timeout)
        if response_time is not None and response_time is not False:
            self.logger.debug(f'Target {target} reached. Response time: {response_time} seconds')
            return True
        else:
            self.logger.debug(f'{target} is not reachable or timed out (timeout={timeout} seconds)')
            return False

    def test(self):
        recording = self.get_recording()
        reachable = self.reachable(self.targets)
        if recording and reachable:
            self.stop_recording()
            self.logger.debug("Stopping recording...")
        elif not reachable and not recording:
            self.start_recording()
            self.logger.debug("Recording time...")
        else:
            self.logger.debug(f"Business as usual")

    def run(self):
        if self.armed:
            # Run reachability check in a separate thread to avoid blocking
            threading.Thread(target=self.test).start()
            # Schedule the next check using Tkinter's after() method
            self.root.after(self.check_interval, self.run)


    def start_recording(self):
        self.t0 = datetime.now()
        self.recording = True
        self.logger.info(f"Failover test started at: {self.t0.strftime('%Y-%m-%d %H:%M:%S')}")


    def stop_recording(self):
        self.t1 = datetime.now()
        self.logger.info(f"Failover test ended at: {self.t1.strftime('%Y-%m-%d %H:%M:%S')}")
        downtime = self.t1 - self.t0
        self.logger.info(f"Connection was down for {downtime.total_seconds()} seconds")
        self.t0 = None
        self.t1 = None
        self.recording = False

    def get_recording(self):
        return self.recording

    def set_recording(self, val):
        self.recording = val

    def get_armed(self):
        return self.armed


