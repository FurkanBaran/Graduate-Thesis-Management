# Graduate Thesis System (GTS)

The Graduate Thesis System (GTS) is a lightweight, rapidly developed database application tailored to effectively manage graduate theses. This project was crafted over a few days upon specific request, utilizing PostgreSQL for backend data management integrated with a Python Flask web application, enhanced with JavaScript and Bootstrap for frontend interactions.

Despite the quick development timeline, the system robustly adheres to detailed database constraints and requirements, ensuring data integrity and compliance with the specified schema rules. The GTS is equipped with numerous functions designed for adding, editing, and deleting records, all while maintaining a user-friendly interface that simplifies database interaction, facilitating efficient data entry, querying, and administration of graduate thesis records.

The application ensures that all interactions are in strict adherence to the database's integrity rules and constraints. Each function is carefully implemented to enforce data consistency and reliability. In instances where user actions might violate these predefined rules, the system provides clear and informative error messages, guiding users to resolve any potential issues effectively. This approach not only enhances the system's usability but also ensures the integrity and accuracy of the data maintained.

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

`psql -U username -d database_name -f pg-database.sql`

Usage

Don't forget to update database credentials. Run the application through your preferred web server or localhost setup. Access the system via the web interface to manage thesis records.
## Screenshots
![image](https://github.com/FurkanBaran/Graduate-Thesis-Management/assets/21145014/f2fc345d-05e2-4fb7-85c2-6ad9cbdb65c0)
![image](https://github.com/FurkanBaran/Graduate-Thesis-Management/assets/21145014/c28b0b00-cc19-43be-b86c-29b691be0abe)
![image](https://github.com/FurkanBaran/Graduate-Thesis-Management/assets/21145014/8f5c1d65-0f59-46b0-be3f-da7d6349d8da)
![image](https://github.com/FurkanBaran/Graduate-Thesis-Management/assets/21145014/331c4413-1903-43c5-b640-70eda73e7796)
![image](https://github.com/FurkanBaran/Graduate-Thesis-Management/assets/21145014/db727ba5-9969-4065-a495-c6008fa242ea)
![image](https://github.com/FurkanBaran/Graduate-Thesis-Management/assets/21145014/c3b57903-4ac7-4480-ac3f-04fb1f4296de)
![image](https://github.com/FurkanBaran/Graduate-Thesis-Management/assets/21145014/f1b5a4a0-87d9-46d9-b609-94a6a18c6d68)
![image](https://github.com/FurkanBaran/Graduate-Thesis-Management/assets/21145014/53aab4f1-f0a4-41f9-931f-df76c705beca)



Contributing
Contributions to the GTS are welcome. Please fork the repository and submit pull requests with your proposed changes.

License
This project is licensed under the MIT License - see the LICENSE.md file for details.


## Note

Please note that this application is a basic implementation and may require further enhancements and security measures before being used in a production environment.

