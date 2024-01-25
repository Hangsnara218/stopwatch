import time
import threading
from PyQt5 import uic
from PyQt5.QtWidgets import *

class GUI(QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi("sw.ui", self)
        self.show()
        self.running = False 
        self.started = False 
        self.passed = 0 
        self.previous_passed = 0 
        self.lap = 1

        self.startBtn.clicked.connect(self.start_stop)
        self.lapBtn.clicked.connect(self.lap_reset)
        self.label.setStyleSheet("border: 5px solid transparent")

    def start_stop(self):
        if self.running:
            self.running = False
            self.startBtn.setText("Resume")
            self.lapBtn.setText("Reset")
        else:
            self.running = True
            self.startBtn.setText("Stop")
            self.lapBtn.setText("Lap")
            self.lapBtn.setEnabled(True)
            threading.Thread(target=self.stopwatch).start()

    def lap_reset(self):
        if self.running:
            self.label.setText(self.label.text() + f"(Lap {self.lap} - Passed: {self.format_time_string(self.passed)}"
                           f" - Difference: {self.format_time_string(self.passed - self.previous_passed)})\n")
            self.lap += 1
            self.previous_passed = self.passed
        else:
            self.startBtn.setText("Start")
            self.lapBtn.setText("Lap") 
            self.lapBtn.setEnabled(False)
            self.label_2.setText("00:00:00:00")
            self.label.setText("Laps: ")
            self.lap = 1


    def format_time_string(self, time_passed):
        sec = time_passed % 60
        min = time_passed // 60
        hour = min // 60
        return f"{int(hour):02d}:{int(min):02d}:{int(sec):02d}:{int((self.passed % 1)*100):02d}"

    def stopwatch(self):
        start = time.time()
        if self.started:
            until_now = self.passed
        else:
            until_now = 0
            self.started = True
        
        while self.running:
            self.passed = time.time() - start + until_now
            self.label_2.setText(self.format_time_string(self.passed))

def main():
    app = QApplication([])
    window = GUI()
    app.exec_()

if __name__ == "__main__":
    main()