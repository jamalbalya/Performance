This Python code snippet presents a function that constructs a user-friendly GUI application utilizing the Tkinter library for testing functionality at a designated URL. The application performs calculations and presents various performance metrics by sending a specified number of requests to the provided URL. The performance metrics include average response time, standard deviation, error percentage, requests per second, minimum response time, and maximum response time.

The code includes the following components:

    The PerformanceTestApp class is defined to configure the graphical user interface (GUI) of the performance test application.
    In the constructor (init) of the PerformanceTestApp class:
        It initializes the main application window and sets its title.
        Based on the screen size, it calculates the window's centre position and sets its geometry accordingly.
        Various widgets, such as labels, entry fields, buttons, and text boxes, are created to display the test results.
        The web manager is utilized to configure these widgets.
        To prevent users from closing the application during the test, the close button (X) in the main window is disabled.
    The validate_entry method is utilized for validating the user's input in the "Number of Req" entry field, allowing only numeric characters and empty strings.
    The validate_url method is used to ensure the provided URL is a valid HTTP or HTTPS URL.
    When the "Process" button is clicked, the start_performance_test method is invoked. It fetches the URL and request number from the input fields, disables all buttons, and opens a pop-up window displaying a "test" message as the test executes.
    The perform_test method is employed to initiate a performance test in a separate thread. It sends multiple HTTP requests to the specified URL and measures their responses.
