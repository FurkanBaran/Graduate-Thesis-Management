# Thesis Management System

This is a Flask web application for managing theses. It was developed as a request project with special requirements and completed in 3-4 days. The application includes all the requested features and meets all the specified requirements.
live demo: https://gts-test.vercel.app/
(Vercel demo uses ElephantSQL which is shutting down in 2025. So demo app will crash after that time.)
## Features

- Index Page: Displays the main page of the application.
- Add Data Page: Allows users to add data to the system.
- Add Person: Handles the addition of a new person to the system.
- Add University: Handles the addition of a new university to the system.
- Add Institute: Handles the addition of a new institute to the system.
- Add Topic: Handles the addition of a new topic to the system.
- Add Thesis: Handles the addition of a new thesis to the system.
- Search Page: Allows users to search for theses based on various criteria.
- Search Thesis: Retrieves the search results based on the user's input.
- Get Thesis Details: Displays the details of a specific thesis.
- Edit Page: Allows users to edit existing data in the system.
- Edit Person: Handles the editing of a person's details.
- Edit Topic: Handles the editing of a topic's details.
- Edit University: Handles the editing of a university's details.
- Edit Institute: Handles the editing of an institute's details.
- Delete Person: Handles the deletion of a person from the system.
- Delete Topic: Handles the deletion of a topic from the system.
- Delete University: Handles the deletion of a university from the system.
- Delete Institute: Handles the deletion of an institute from the system.

## Usage

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Set up the PostgreSQL database connection by modifying the `conn` variable in the code.
3. Run the application by executing `python app.py`.
4. Access the application in your web browser at `http://localhost:5000`.

## Note

Please note that this application is a basic implementation and may require further enhancements and security measures before being used in a production environment.
