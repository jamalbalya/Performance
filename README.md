This code is a Python function that creates a simple GUI application that uses the Tkinter library to test functionality at a given URL. The application calculates and displays various performance metrics when it sends a specified number of requests to a given URL, such as average response time, standard deviation, error percentage, requests per second, responses minimum time, and maximum response time

    Defines the PerformanceTestApp class that configures the graphical user interface (GUI) for the performance test application.

    In the Constructor (__init__) of the PerformanceTestApp class:
        It starts the main application window and sets its title.
        Based on the screen size it calculates the center position of the window and sets its geometry.
        It creates a variety of widgets such as labels, entry fields, buttons, and text boxes to display test results.
        It uses the web manager to configure widgets.
        Disables the close button (X) in the main window to prevent users from closing the application while the test is running.

    The validate_entry method is used to validate the user's entry in the "Number of Req" entry field. It only allows digital characters and empty strings.

    The validate_url method is used to verify that the given URL is a valid HTTP or HTTPS URL.

    Clicking the "Process" button calls the start_performance_test method. It retrieves the URL and request number from the input field, disables all the buttons, and opens a pop-up window to display a "test" message as the test executes

    The perform_test method is used to start a performance test in a separate thread. It sends multiple HTTP requests to a given URL, measures their response