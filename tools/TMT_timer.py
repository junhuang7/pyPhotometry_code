# @Author: Jun HUANG, 2023.07.12
# This code is for timing the TMT experiments

import tkinter as tk
from datetime import datetime, timedelta

data = {
        'UniBe001': 
            {'Stim': [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0], 
             'Time': ['00:30', '01:28', '01:59', '02:29', '03:23', '03:57', '04:36', '05:24', '06:24', '07:23', 
                      '08:10', '08:56', '09:39', '10:13', '10:54', '11:33', '12:15', '13:00', '13:34', '14:11', 
                      '15:03', '15:35', '16:09', '16:42', '17:38', '18:09', '18:51', '19:22', '20:00', '20:59']}, 
        'UniBe002': 
            {'Stim': [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1], 
             'Time': ['00:30', '01:05', '01:53', '02:25', '03:25', '04:16', '05:10', '05:59', '06:35', '07:19', 
                      '08:17', '08:54', '09:50', '10:36', '11:30', '12:13', '12:48', '13:31', '14:16', '15:15', 
                      '16:08', '17:03', '17:44', '18:27', '19:24', '20:21', '20:53', '21:27', '22:09', '23:07']}, 
        'UniBe003': 
            {'Stim': [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0], 
             'Time': ['00:30', '01:17', '01:47', '02:28', '03:11', '03:43', '04:19', '04:59', '05:32', '06:29', 
                      '07:28', '08:11', '08:42', '09:23', '10:18', '11:13', '12:04', '13:00', '13:36', '14:22', 
                      '15:13', '16:11', '16:52', '17:40', '18:14', '18:47', '19:36', '20:32', '21:22', '22:13']}, 
        'UniBe004': 
            {'Stim': [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0], 
             'Time': ['00:30', '01:29', '02:07', '02:48', '03:39', '04:19', '04:59', '05:46', '06:20', '06:50', 
                      '07:49', '08:38', '09:37', '10:19', '11:16', '12:03', '12:42', '13:34', '14:08', '14:53', 
                      '15:25', '16:12', '16:56', '17:41', '18:11', '19:06', '19:43', '20:27', '21:02', '22:02']}, 
        'UniBe005': 
            {'Stim': [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0] ,
            'Time': ['00:30', '01:25', '02:24', '03:12', '03:45', '04:17', '04:52', '05:38', '06:09', '06:44', 
                    '07:30', '08:17', '08:49', '09:42', '10:31', '11:30', '12:26', '13:23', '14:11', '15:08', 
                    '15:57', '16:30', '17:10', '18:06', '18:39', '19:33', '20:25', '21:21', '22:01', '22:34'] }, 
        'UniBe006': 
            {'Stim': [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1], 
             'Time': ['00:30', '01:25', '02:22', '03:00', '03:46', '04:45', '05:44', '06:16', '06:47', '07:19', 
                    '08:07', '08:53', '09:39', '10:30', '11:21', '12:06', '12:38', '13:16', '14:08', '14:57', 
                    '15:48', '16:40', '17:26', '18:04', '18:56', '19:49', '20:29', '21:22', '22:22', '23:17']}, 
        'UniBe007': 
            {'Stim': [0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
             'Time': ['00:30', '01:09', '01:42', '02:21', '03:15', '04:06', '05:03', '05:47', '06:17', '07:13', 
                    '08:02', '08:32', '09:05', '09:44', '10:25', '11:03', '11:45', '12:18', '12:54', '13:44',
                    '14:34', '15:05', '15:39', '16:14', '17:02', '17:37', '18:33', '19:14', '19:58', '20:52']}, 
        'UniBe008': {
            'Stim': [0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0],
            'Time': ['00:30', '01:14', '01:55', '02:44', '03:23', '04:22', '05:10', '06:02', '06:55', '07:39', 
                    '08:34', '09:17', '10:08', '10:51', '11:45', '12:44', '13:28', '14:05', '15:00', '15:50', 
                    '16:35', '17:24', '18:09', '19:03', '19:39', '20:30', '21:06', '21:55', '22:31', '23:18']},

        'UniBe009': 
            {'Stim': [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0], 
             'Time': ['00:30', '01:24', '02:11', '03:01', '03:57', '04:31', '05:23', '06:07', '07:01', '07:42', 
                    '08:21', '08:54', '09:45', '10:21', '11:21', '11:56', '12:42', '13:42', '14:20', '15:02', 
                    '15:49', '16:27', '17:16', '17:49', '18:32', '19:28', '20:17', '20:51', '21:21', '22:14'] }, 

        'UniBe010': 
            {'Stim': [1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1], 
             'Time': ['00:30', '01:28', '02:08', '02:43', '03:28', '03:59', '04:33', '05:32', '06:11', '06:54', 
                    '07:39', '08:25', '09:01', '09:51', '10:48', '11:43', '12:25', '13:09', '13:55', '14:54', 
                    '15:36', '16:26', '17:14', '18:04', '18:35', '19:05', '19:52', '20:48', '21:19', '21:59'] }, 

        'UniBe011': 
            {'Stim': [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1], 
             'Time': ['00:30', '01:06', '01:43', '02:19', '03:13', '03:46', '04:46', '05:20', '06:02', '06:43', 
                    '07:28', '08:28', '09:21', '10:13', '11:12', '12:01', '13:00', '13:34', '14:11', '14:48', 
                    '15:26', '16:03', '16:51', '17:46', '18:38', '19:30', '20:27', '21:21', '22:09', '22:58']}, 

        'UniBe012': 
            {'Stim': [0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1], 
             'Time': ['00:30', '01:02', '01:47', '02:39', '03:22', '04:17', '05:04', '05:52', '06:39', '07:10', 
                    '07:42', '08:14', '09:10', '10:03', '10:39', '11:23', '12:15', '12:56', '13:52', '14:31', 
                    '15:07', '15:42', '16:37', '17:17', '18:15', '19:09', '20:08', '20:39', '21:19', '22:12']}, 

        'UniBe013': 
            {'Stim': [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0], 
             'Time': ['00:30', '01:06', '01:49', '02:29', '03:04', '04:01', '04:40', '05:25', '06:12', '06:48',
                     '07:34', '08:31', '09:10', '09:52', '10:43', '11:24', '12:00', '12:41', '13:13', '13:58', 
                     '14:53', '15:29', '16:16', '17:03', '17:48', '18:23', '18:57', '19:56', '20:46', '21:18']}}

class TimerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer GUI")
        self.current_set = None
        self.timer_running = False
        self.remaining_time = timedelta()
        self.upcoming_events = []

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Set Selection
        self.label_set = tk.Label(self.frame, text="Select Set:")
        self.label_set.grid(row=0, column=0, sticky="W")

        self.set_var = tk.StringVar()
        self.set_var.set("Select a set")
        self.set_dropdown = tk.OptionMenu(self.frame, self.set_var, *data.keys(), command=self.on_set_select)
        self.set_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="W")

        # Timer
        self.timer_label = tk.Label(self.frame, text="00:00", font=("Arial", 200), width=10)
        self.timer_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Upcoming Event
        self.event_label = tk.Label(self.frame, text="", font=("Arial", 100), fg="red")
        self.event_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Next Event Type
        self.event_type_label = tk.Label(self.frame, text="", font=("Arial", 100))
        self.event_type_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Begin Button
        self.begin_button = tk.Button(self.frame, text="Begin", command=self.start_timer, state=tk.DISABLED)
        self.begin_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def on_set_select(self, selected_set):
        self.current_set = selected_set
        self.begin_button["state"] = tk.NORMAL
        first_event_type = "TMT" if data[self.current_set]["Stim"][0] == 1 else "Saline"
        self.event_type_label["text"] = f"First Event Type: {first_event_type}"

    def start_timer(self):
        if self.current_set:
            self.timer_running =True
            self.begin_button["state"] = tk.DISABLED
            self.remaining_time = timedelta(seconds=0)
            self.upcoming_events = [datetime.strptime(t, "%M:%S") for t in data[self.current_set]["Time"]]
            self.countup()

    def countup(self):
        if self.timer_running:
            self.remaining_time += timedelta(seconds=1)
            self.timer_label["text"] = str(self.remaining_time)[2:]

            if self.upcoming_events:
                upcoming_event = self.upcoming_events[0]
                time_diff = upcoming_event - datetime.strptime(str(self.remaining_time)[2:], "%M:%S")

                if time_diff <= timedelta(seconds=30):
                    self.event_label["text"] = f"Upcoming Event: {upcoming_event.strftime('%M:%S')} ({time_diff.seconds}s)"
                    event_index = len(data[self.current_set]["Time"]) - len(self.upcoming_events)
                    if data[self.current_set]["Stim"][event_index] == 1:
                        self.event_type_label["text"] = "Next Event Type: TMT"
                    else:
                        self.event_type_label["text"] = "Next Event Type: Saline"
                else:
                    self.event_label["text"] = ""
                    self.event_type_label["text"] = ""

                if time_diff <= timedelta(seconds=0):
                    self.upcoming_events.pop(0)
            if self.timer_running:
                self.root.after(991, self.countup)

    def stop_timer(self):
        self.timer_running = False

root = tk.Tk()
root.attributes("-fullscreen", True)  # Make the GUI full screen
app = TimerGUI(root)
root.mainloop()