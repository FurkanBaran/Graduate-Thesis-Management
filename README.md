# Graduate Thesis System (GTS)

The Graduate Thesis System (GTS) is a comprehensive database application developed to manage graduate theses effectively. This project was rapidly developed over a few days upon request and utilizes PostgreSQL for backend data management. The application provides a user-friendly web interface for interacting with the database, facilitating efficient data entry, querying, and administration of graduate thesis records.

live demo: https://gts-test.vercel.app/
(Vercel demo uses ElephantSQL which is shutting down in 2025. So demo app will crash after that time.)


## Features

- **Index Page**: Displays the main page of the application, serving as the entry point for users.
- **Add Data Page**: Allows users to add various types of data to the system, streamlining the process of populating the database.
- **Add Person**: Manages the addition of new people to the system, including students, faculty, or researchers.
- **Add University**: Facilitates the creation of new university entries in the database.
- **Add Institute**: Enables users to add new institutes associated with universities.
- **Add Topic**: Allows for the addition of new subject topics to categorize the theses.
- **Add Thesis**: Manages the addition of new theses, linking them to authors, topics, and other relevant details.
- **Search Page**: Provides a search interface for users to find theses based on various criteria such as title, author, year, etc.
- **Search Thesis**: Retrieves and displays search results based on user input.
- **Get Thesis Details**: Shows detailed information for a specific thesis, including abstract, author, year, and status.
- **Edit Page**: Offers functionalities to edit existing records in the database.
- **Edit Person**: Allows for modifications to person details.
- **Edit Topic**: Enables editing details of existing topics.
- **Edit University**: Manages the updating of university details.
- **Edit Institute**: Facilitates the editing of institute details.
- **Delete Person**: Handles the removal of a person from the system.
- **Delete Topic**: Allows for the deletion of topics from the system.
- **Delete University**: Manages the deletion of university records.
- **Delete Institute**: Handles the removal of institute records.

## Installation

To set up the GTS, follow these steps:

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Import the provided SQL file into your PostgreSQL database to create and populate the database schema.
3. Set up the PostgreSQL database connection by modifying the `conn` variable in the code.
4. Run the application by executing `python app.py`.
5. Access the application in your web browser at `http://localhost:5000`.

psql -U username -d database_name -f pg-database.sql
Usage
Don't forget to update database credentials. Run the application through your preferred web server or localhost setup. Access the system via the web interface to manage thesis records.

Contributing
Contributions to the GTS are welcome. Please fork the repository and submit pull requests with your proposed changes.

License
This project is licensed under the MIT License - see the LICENSE.md file for details.


## Note

Please note that this application is a basic implementation and may require further enhancements and security measures before being used in a production environment.

