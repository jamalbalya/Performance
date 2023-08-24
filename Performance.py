import time
import threading
import requests
import tkinter as tk
from tkinter import ttk
from urllib.parse import urlparse
import statistics

class PerformanceTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Performance Test By Jamal Balya v1.0.1")

        # Calculate the center position of the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 500
        window_height = 350
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.url_label = ttk.Label(self.root, text="URL:")
        self.url_entry = ttk.Entry(self.root, width=30)
        self.url_entry.insert(0, "https://")
        self.requests_label = ttk.Label(self.root, text="Number of Req:")
        self.requests_entry = ttk.Entry(self.root, width=30)

        # Add a validation command to the "Number of Req" entry
        self.requests_entry.config(validate="key", validatecommand=(self.root.register(self.validate_entry), "%P"))

        self.requests_entry.insert(0, "")

        self.process_button = ttk.Button(self.root, text="Process", command=self.start_performance_test)
        self.output_text = tk.Text(self.root, wrap=tk.WORD, width=50, height=10, state=tk.DISABLED, bd=1, relief=tk.SOLID)
        self.close_button = ttk.Button(self.root, text="Close", command=self.root.quit)

        self.url_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.url_entry.grid(row=0, column=1, columnspan=3, pady=10, sticky="w")

        self.requests_label.grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.requests_entry.grid(row=1, column=1, columnspan=3, pady=10, sticky="w")

        self.process_button.grid(row=2, column=0, columnspan=4, pady=5)

        self.output_text.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")  # Use sticky="nsew"

        self.close_button.grid(row=4, column=0, columnspan=4, pady=5, sticky="nsew")  # Use sticky="nsew"

        # Configure row and column weights to make the widgets expand and fill the available space
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # Disable the "x" button (close button) on the main window
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

    def validate_entry(self, value):
        return value.isdigit() or value == ""

    def validate_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc]) and result.scheme in ["http", "https"]
        except:
            return False

    def start_performance_test(self):
        url = self.url_entry.get()
        num_requests = int(self.requests_entry.get())

        # Disable all buttons
        self.process_button.config(state=tk.DISABLED)
        self.close_button.config(state=tk.DISABLED)

        # Show the popup window message
        popup_window = tk.Toplevel(self.root)
        popup_window.title("Testing")
        popup_window.transient(self.root)  # Set as transient for the main window
        popup_window.grab_set()  # Set as a modal dialog

        # Calculate the center position of the popup window relative to the main window
        popup_width = 400
        popup_height = 200
        popup_x_position = self.root.winfo_x() + (self.root.winfo_width() - popup_width) // 2
        popup_y_position = self.root.winfo_y() + (self.root.winfo_height() - popup_height) // 2

        # Calculate the center position of the main window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        main_x_position = (screen_width - popup_width) // 2
        main_y_position = (screen_height - popup_height) // 2

        # Adjust the popup window position to be centered on the main window
        popup_window.geometry(f"{popup_width}x{popup_height}+{main_x_position}+{main_y_position}")

        popup_label = tk.Label(popup_window, text="On Progress......")
        popup_label.pack(pady=20)

        # Start the performance test on a separate thread
        threading.Thread(target=self.perform_test, args=(url, num_requests, popup_window)).start()

    def perform_test(self, url, num_requests, popup_window):
        # Start the performance test
        response_times = []
        responses = []

        for _ in range(num_requests):
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            response_time = end_time - start_time
            responses.append(response)
            response_times.append(response_time)

        # Calculate metrics
        average_response_time = statistics.mean(response_times)
        std_dev_response_time = statistics.stdev(response_times) if len(response_times) > 1 else 0.0
        error_percentage = (response_times.count(0) / num_requests) * 100
        requests_per_second = num_requests / sum(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)

        received_kb_per_sec = sum(len(response.content) / 1024 for response in responses) / sum(response_times)
        sent_kb_per_sec = 0  # Calculate based on your payload
        avg_bytes = sum(len(response.content) for response in responses) / len(responses)

        # Update the result in the output text
        self.root.after(0, self.update_result, average_response_time, std_dev_response_time, error_percentage, requests_per_second, min_response_time, max_response_time, received_kb_per_sec, sent_kb_per_sec, avg_bytes)

        # Close the popup window and enable all buttons
        self.root.after(0, popup_window.destroy)
        self.root.after(0, self.enable_buttons)

    def update_result(self, average_response_time, std_dev_response_time, error_percentage, requests_per_second, min_response_time, max_response_time, received_kb_per_sec, sent_kb_per_sec, avg_bytes):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Average Response Time: {average_response_time:.2f} seconds\n")
        self.output_text.insert(tk.END, f"Min Response Time: {min_response_time:.2f} seconds\n")
        self.output_text.insert(tk.END, f"Max Response Time: {max_response_time:.2f} seconds\n")
        self.output_text.insert(tk.END, f"Standard Deviation: {std_dev_response_time:.2f}\n")
        self.output_text.insert(tk.END, f"Error Percentage: {error_percentage:.2f}%\n")
        self.output_text.insert(tk.END, f"Throughput: {requests_per_second:.2f} requests per second\n")
        self.output_text.insert(tk.END, f"Received KB/sec: {received_kb_per_sec:.2f} KB/sec\n")
        self.output_text.insert(tk.END, f"Sent KB/sec: {sent_kb_per_sec:.2f} KB/sec\n")
        self.output_text.insert(tk.END, f"Avg. Bytes: {avg_bytes:.2f} bytes\n")

        self.output_text.config(state=tk.DISABLED)

    def enable_buttons(self):
        self.process_button.config(state=tk.NORMAL)
        self.close_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = PerformanceTestApp(root)
    root.mainloop()
