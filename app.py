from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(
    host="host",
    database="database",
    user="user",
    password="password"
)
# get a cursor from the database connection
conn.autocommit = True
conn.set_client_encoding('UTF8')
cur=conn.cursor()


# Index Page
@app.route('/')
def index():
    
    try:
        cur.execute("SELECT thesis_no, author_id,title, TYPE, year, language, num_pages FROM Theses")
        result = cur.fetchall()
        # Get column names from cursor description
        column_names = [desc[0] for desc in cur.description]
        # Convert result to dictionary format
        result = [dict(zip(column_names, row)) for row in result]
        return render_template('search_result.html', homepage=True, response=result)
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
   


# add data page
@app.route('/add_data')
def add_data():
    # get university names 
    cur.execute("SELECT university_id, name FROM Universities")
    universities = cur.fetchall()
    # get institute names
    cur.execute("SELECT institute_id, name, university_id FROM institutes")
    institutes = cur.fetchall()
    # get person names
    cur.execute("SELECT person_id, name FROM persons")
    persons = cur.fetchall()
    # get topic names
    cur.execute("SELECT topic_id ,topic_name FROM subjecttopics")    
    topics = cur.fetchall()

    return render_template('add_data.html', uni_list=universities, ins_list=institutes, person_list=persons, topic_list=topics)


# add person
@app.route('/add_person', methods=['POST'])
def add_person():
    title = request.form.get('title')
    name = request.form.get('name')
    try:
        cur.execute("INSERT INTO Persons(title, name) VALUES(%s, %s)", (title, name))
    
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="Person added successfully")

# add university
@app.route('/add_university', methods=['POST'])
def add_university():
    name = request.form.get('name')
    try:
        cur.execute("INSERT INTO Universities(name) VALUES(%s)", (name,))
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="University added successfully")

# add institute
@app.route('/add_institute', methods=['POST'])
def add_institute():
    name = request.form.get('name')
    uni_id = request.form.get('uni_id')
    try:
        cur.execute("INSERT INTO Institutes(name, university_id) VALUES(%s, %s)", (name, uni_id))
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="Institute added successfully")


# add topic
@app.route('/add_topic', methods=['POST'])
def add_topic():
    name = request.form.get('name')
    # if topic already exists, return error
    cur.execute("SELECT topic_name FROM SubjectTopics WHERE topic_name = %s", (name,))
    if cur.fetchone():
        return render_template('result.html', response="Topic already exists.", error=True)
    try:
        cur.execute("INSERT INTO SubjectTopics(topic_name) VALUES(%s)", (name,))
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="Topic added successfully")


# add thesis
@app.route('/add_thesis', methods=['POST'])
def add_thesis():
    '''
    Add a thesis to the database.
    if thesis and its related data are valid, add the thesis to the theses table, related data to the related tables.
    if any error occurs, rollback the operation and return the error message.
    '''
    # Retrieve thesis details from the request

    title = request.form.get('title')
    abstract = request.form.get('abstract')
    author = request.form.get('author')
    year = request.form.get('year')
    type = request.form.get('type')
    uni = request.form.get('uni')
    ins = request.form.get('ins')
    num_pages = request.form.get('num_pages')
    language = request.form.get('language')
    supervisors = request.form.getlist('supervisors')
    cosupervisors = request.form.getlist('cosupervisors')
    topics = request.form.getlist('topics')
    keywords = request.form.get('keywords')
    # at least one supervisor is required
    if not supervisors:
         return render_template('result.html', response=( "At least one supervisor is required."), error=True)
    if not topics:
        return render_template('result.html', response=( "At least one topic is required."), error=True)
    
    # Convert author, supervisors and cosupervisors to integer list
    author_id = int(author)  
    supervisor_ids = [int(sup) for sup in supervisors] 
    cosupervisor_ids = [int(cosup) for cosup in cosupervisors]  

    # Create a union set of all persons
    all_persons = set([author_id] + supervisor_ids + cosupervisor_ids)

    cur.execute("SELECT person_id FROM Persons WHERE person_id = ANY(%s);", (list(all_persons),))
    valid_persons = set([row[0] for row in cur.fetchall()])
    if len(all_persons) > len(valid_persons):
        return render_template('result.html', response=( "Some persons (author, supervisors, cosupervisors) are not found in the Persons table."), error=True)

    topics_int = [int(topic) for topic in topics]

    # Check topics in SubjectTopics table
    cur.execute("SELECT topic_id FROM SubjectTopics WHERE topic_id = ANY(%s);", (topics_int,))
    valid_topics = [row[0] for row in cur.fetchall()]

    if len(valid_topics) != len(topics):
        return render_template('result.html', response=( "Some topics are not found in the SubjectTopics table."), error=True)


    # Each supervisor, cosupervisor and author must be different from each other
    if len(set(supervisors).intersection(cosupervisors)) > 0 or author in supervisors or author in cosupervisors:

        return render_template('result.html', response=("Author, supervisors, and cosupervisors must be different."), error=True)
    # set submission date to current date
    submission_date = "now()"

    try:
        # Add data to the Thesis table
        cur.execute(
            """
            INSERT INTO Theses(title, abstract, author_id, year, type, university_id, institute_id, num_pages, language, submission_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING thesis_no;
            """,
            (title, abstract, author, year, type, uni, ins, num_pages, language, submission_date)
        )
        thesis_no = cur.fetchone()[0]

        try:
            # Add data to the Supervisors table
            for supervisor in supervisors:
                cur.execute(
                    "INSERT INTO Supervisors (thesis_no, supervisor) VALUES (%s, %s);",
                    (thesis_no, supervisor)
                )

            # Add data to the CoSupervisors table
            for cosupervisor in cosupervisors:
                cur.execute(
                    "INSERT INTO CoSupervisors (thesis_no, cosupervisor) VALUES (%s, %s);",
                    (thesis_no, cosupervisor)
                )

            # Add data to the ThesisSubjectTopics table
            for topic in topics_int:
                cur.execute(
                    "INSERT INTO ThesisSubjectTopics (thesis_no, topic_id) VALUES (%s, %s);",
                    (thesis_no, topic)
                )

            # Add data to the Keywords table and ThesisKeywords table
            for keyword in keywords.split(","):
                keyword = keyword.strip()  # Trim whitespace
                if keyword:  # Skip empty strings
                    cur.execute("INSERT INTO Keywords (keyword) VALUES (%s) ON CONFLICT (keyword) DO NOTHING RETURNING keyword_id;", (keyword,))
                    keyword_id = cur.fetchone()
                    if keyword_id:
                        cur.execute(
                            "INSERT INTO ThesisKeywords (thesis_no, keyword_id) VALUES (%s, %s);",
                            (thesis_no, keyword_id[0])
                        )

            # Commit the operations and close the connection   
            conn.commit()
        except psycopg2.errors.RaiseException as e:
            # rollback the add thesis operation
            conn.rollback()
            return render_template('result.html', response=(e), error=True)
        

        return render_template('result.html', response="Thesis added successfully. Thesis No: "+str(thesis_no))
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)




# search page
@app.route('/search', methods=['GET'])
def search2():
    # get university names 
    cur.execute("SELECT university_id, name FROM Universities")
    universities = cur.fetchall()
    # query that gets institute names and its university name
    cur.execute("SELECT institutes.institute_id, institutes.name, institutes.university_id, universities.name FROM institutes INNER JOIN universities ON institutes.university_id = universities.university_id")
    institutes = cur.fetchall()
    # get person names
    cur.execute("SELECT person_id, title, name FROM persons")
    persons = cur.fetchall()
    # get topic names
    cur.execute("SELECT topic_id ,topic_name FROM subjecttopics")    
    topics = cur.fetchall()
    return render_template('search.html', uni_list=universities, ins_list=institutes, person_list=persons, topic_list=topics)
    

# get data from form, generate a query and return the result
@app.route('/search_thesis', methods=['POST'])
def search_thesis():
    conditions=request.form.to_dict()
    try:
        query = generate_search_query(conditions)
    except ValueError as e:
        return render_template('result.html', response=(e), error=True)
    try:
        cur.execute(query)
        result = cur.fetchall()
        # Get column names from cursor description
        column_names = [desc[0] for desc in cur.description]
        # Convert result to dictionary format
        result = [dict(zip(column_names, row)) for row in result]
        return render_template('search_result.html', response=result)
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)

    

@app.route('/get_thesis/<string:id>', methods=['GET'])
def get_thesis(id):
    try:
        # Thesis details query
        cur.execute('''SELECT 
        Theses.thesis_no,
        Persons.title || ' ' || Persons.name AS author_name,
        SupervisorPerson.NAME AS supervisor_name,
        CoSupervisorPerson.NAME AS cosupervisor_name,
        Theses.title,
        Theses.abstract,
        Universities.NAME AS university_name,
        Institutes.NAME AS institute_name,
        Theses.submission_date,
        Theses.num_pages,
        Theses.language,
        Theses.year,
        Theses.type
        FROM 
            Theses
        LEFT JOIN 
            Persons ON Theses.author_id = Persons.person_id
        LEFT JOIN 
            Supervisors ON Theses.thesis_no = Supervisors.thesis_no
        LEFT JOIN 
            Persons SupervisorPerson ON Supervisors.supervisor = SupervisorPerson.person_id
        LEFT JOIN 
            CoSupervisors ON Theses.thesis_no = CoSupervisors.thesis_no
        LEFT JOIN 
            Persons CoSupervisorPerson ON CoSupervisors.cosupervisor = CoSupervisorPerson.person_id
        LEFT JOIN 
            Universities ON Theses.university_id = Universities.university_id
        LEFT JOIN 
            Institutes ON Theses.institute_id = Institutes.institute_id
        WHERE 
            Theses.thesis_no = %s;''', (id,))
        thesis_details = cur.fetchall()
        if not thesis_details:
            return render_template('result.html', response="Thesis not found.", error=True)
        
        thesis_details_dict = dict(zip([desc[0] for desc in cur.description], thesis_details[0]))

        # Keywords query
        cur.execute('''SELECT 
                Keywords.keyword
            FROM 
                ThesisKeywords
            LEFT JOIN 
                Keywords ON ThesisKeywords.keyword_id = Keywords.keyword_id
            WHERE 
                ThesisKeywords.thesis_no = %s;''', (id,))
        keywords = [item[0] for item in cur.fetchall()]

        # Topics query
        cur.execute('''SELECT 
                SubjectTopics.topic_name
            FROM 
                ThesisSubjectTopics
            LEFT JOIN 
                SubjectTopics ON ThesisSubjectTopics.topic_id = SubjectTopics.topic_id
            WHERE 
                ThesisSubjectTopics.thesis_no = %s;''', (id,))
        topics = [item[0] for item in cur.fetchall()]

        result = {'thesis': thesis_details_dict, 'keywords': keywords, 'topics': topics}
        return render_template('thesis.html', result=result)

    except Exception as e:
        return render_template('result.html', response=str(e), error=True)




@app.route('/edit')
def edit():
    # get university names 
    cur.execute("SELECT university_id, name FROM Universities")
    universities = cur.fetchall()
    # query that gets institute names and its university name
    cur.execute("SELECT institutes.institute_id, institutes.name, institutes.university_id, universities.name FROM institutes INNER JOIN universities ON institutes.university_id = universities.university_id")
    institutes = cur.fetchall()
    # get person names
    cur.execute("SELECT person_id, title, name FROM persons")
    persons = cur.fetchall()
    # get topic names
    cur.execute("SELECT topic_id ,topic_name FROM subjecttopics")    
    topics = cur.fetchall()
    # get keywords
    cur.execute("SELECT keyword_id, keyword FROM keywords")

    return render_template('edit.html', uni_list=universities, ins_list=institutes, person_list=persons, topic_list=topics, keyword_list=cur.fetchall())





# Edit Person
@app.route('/edit_person/<int:id>', methods=['POST'])
def edit_person(id):
    title = request.form.get('title')
    name = request.form.get('name')
    try:
        cur.execute("UPDATE Persons SET title = %s, name = %s WHERE person_id = %s", (title, name, id))
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="Person updated successfully")

# Edit Topic
@app.route('/edit_topic/<int:id>', methods=['POST'])
def edit_topic(id):
    name = request.form.get('name')
    try:
        cur.execute("UPDATE SubjectTopics SET topic_name = %s WHERE topic_id = %s", (name, id))
    except psycopg2.errors.ForeignKeyViolation as e:
        return render_template('result.html', response=(e), error=True)
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="Topic updated successfully")

# Edit University
@app.route('/edit_university/<int:id>', methods=['POST'])
def edit_university(id):
    name = request.form.get('name')
    try:
        cur.execute("UPDATE Universities SET name = %s WHERE university_id = %s", (name, id))
    except psycopg2.errors.ForeignKeyViolation as e:
        return render_template('result.html', response=(e), error=True)
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="University updated successfully")

# Edit Institute
@app.route('/edit_institute/<int:id>', methods=['POST'])
def edit_institute(id):
    name = request.form.get('name')
    uni_id = request.form.get('university')
    try:
        cur.execute("UPDATE Institutes SET name = %s, university_id = %s WHERE institute_id = %s", (name, uni_id, id))
    except psycopg2.errors.ForeignKeyViolation as e:
        return render_template('result.html', response=(e), error=True)
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="Institute updated successfully")

# Delete Person
@app.route('/delete_person/<int:id>', methods=['POST'])
def delete_person(id):
    try:
        cur.execute("DELETE FROM Persons WHERE person_id = %s", (id,))
    except psycopg2.errors.ForeignKeyViolation as e:
        return render_template('result.html', response=(e), error=True)
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="Person deleted successfully")

# Delete Topic
@app.route('/delete_topic/<int:id>', methods=['POST'])
def delete_topic(id):
    try:
        cur.execute("DELETE FROM SubjectTopics WHERE topic_id = %s", (id,))
    except psycopg2.errors.ForeignKeyViolation as e:
        return render_template('result.html', response=(e), error=True)
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="Topic deleted successfully")

# Delete University
@app.route('/delete_university/<int:id>', methods=['POST'])
def delete_university(id):
    try:
        cur.execute("DELETE FROM Universities WHERE university_id = %s", (id,))
    except psycopg2.errors.ForeignKeyViolation as e:
        return render_template('result.html', response=(e), error=True)
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="University deleted successfully")

# Delete Institute
@app.route('/delete_institute/<int:id>', methods=['POST'])
def delete_institute(id):
    try:
        cur.execute("DELETE FROM Institutes WHERE institute_id = %s", (id,))
    except psycopg2.errors.ForeignKeyViolation as e:
        return render_template('result.html', response=(e), error=True)
    except psycopg2.errors.RaiseException as e:
        return render_template('result.html', response=(e), error=True)
    return render_template('result.html', response="Institute deleted successfully")



# Generate a SQL query based on the form data.
def generate_search_query(form_data): 
   
    if not form_data or all(not v for v in form_data.values()):
        raise ValueError("At least one search parameter must be provided")

    base_query = "SELECT DISTINCT Theses.thesis_no, Theses.author_id, Theses.title, Theses.TYPE, Theses.year, Theses.LANGUAGE, Theses.num_pages FROM Theses"
    conditions = []

    if form_data.get('uni'):
        conditions.append(f"university_id = {form_data['uni']}")
    if form_data.get('ins'):
        conditions.append(f"institute_id = {form_data['ins']}")
    if form_data.get('author'):
        conditions.append(f"author_id = {form_data['author']}")
    if form_data.get('title'):
        conditions.append(f"title LIKE '%{form_data['title']}%'")
    if form_data.get('abstract'):
        conditions.append(f"abstract LIKE '%{form_data['abstract']}%'")
    if form_data.get('type'):
        conditions.append(f"TYPE = '{form_data['type']}'")
    if form_data.get('language'):
        conditions.append(f"LANGUAGE = '{form_data['language']}'")
    if form_data.get('year'):
        conditions.append(f"year = {form_data['year']}")

    if form_data.get('topic'):
        base_query += " INNER JOIN ThesisSubjectTopics ON Theses.thesis_no = ThesisSubjectTopics.thesis_no"
        conditions.append(f"ThesisSubjectTopics.topic_id = {form_data['topic']}")

    if form_data.get('keywords'):
        base_query += " INNER JOIN ThesisKeywords ON Theses.thesis_no = ThesisKeywords.thesis_no"
        keywords = form_data['keywords'].split(',')
        keyword_conditions = [f"ThesisKeywords.keyword_id IN (SELECT keyword_id FROM Keywords WHERE keyword = '{keyword.strip()}')" for keyword in keywords]
        conditions.append(f"({' OR '.join(keyword_conditions)})")

    query = base_query
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    return query



if __name__ == '__main__':
    app.run(debug=True)

