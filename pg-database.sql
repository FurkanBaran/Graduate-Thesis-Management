-- Persons
CREATE TABLE Persons (
    person_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    NAME VARCHAR(255) NOT NULL
);

-- Universities  
CREATE TABLE Universities (
    university_id SERIAL PRIMARY KEY,
    NAME VARCHAR(255) NOT NULL
);

-- Institutes 
CREATE TABLE Institutes (
    institute_id SERIAL PRIMARY KEY,
    NAME VARCHAR(255) NOT NULL,
    university_id INTEGER REFERENCES Universities(university_id) CHECK (university_id IS NOT NULL)
);

--  Theses
CREATE TABLE Theses (
    thesis_no SERIAL PRIMARY KEY CHECK (thesis_no >= 0 AND thesis_no <= 9999999),
    title VARCHAR(500) NOT NULL,
    abstract VARCHAR(5000) NOT NULL,
    author_id INTEGER REFERENCES Persons(person_id),
    year INTEGER NOT NULL,
    TYPE VARCHAR(50) CHECK (TYPE IN ('Master', 'Doctorate', 'Specialization in Medicine', 'Proficiency in Art')),
    university_id INTEGER REFERENCES Universities(university_id),
    institute_id INTEGER REFERENCES Institutes(institute_id),
    num_pages INTEGER,
    LANGUAGE VARCHAR(50) CHECK (LANGUAGE IN ('Turkish', 'English', 'French')),
    submission_date DATE
);

-- Supervisors
CREATE TABLE Supervisors (
    thesis_no INTEGER REFERENCES Theses(thesis_no),
    supervisor INTEGER REFERENCES Persons(person_id),
    PRIMARY KEY (thesis_no, supervisor)
);

-- CoSupervisors
CREATE TABLE CoSupervisors (
    thesis_no INTEGER REFERENCES Theses(thesis_no),
    cosupervisor INTEGER REFERENCES Persons(person_id),
    PRIMARY KEY (thesis_no, cosupervisor)
);



-- SubjectTopics
CREATE TABLE SubjectTopics (
    topic_id SERIAL PRIMARY KEY,
    topic_name VARCHAR(255) NOT NULL
);
-- ThesisSubjectTopics
CREATE TABLE ThesisSubjectTopics (
    thesis_no INTEGER REFERENCES Theses(thesis_no),
    topic_id INTEGER REFERENCES SubjectTopics(topic_id),
    PRIMARY KEY (thesis_no, topic_id)
);
-- Keywords
CREATE TABLE Keywords (
    keyword_id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL UNIQUE  
);

-- ThesisKeywords
CREATE TABLE ThesisKeywords (
    thesis_no INTEGER REFERENCES Theses(thesis_no),
    keyword_id INTEGER REFERENCES Keywords(keyword_id),
    PRIMARY KEY (thesis_no, keyword_id)
);

-- TRIGGERS --
-- Checks if an authors theses's dates are in logical order
-- Trigger Creation
CREATE OR REPLACE FUNCTION check_thesis_publish_date()
RETURNS TRIGGER AS $$
BEGIN
    -- Master's Thesis Publication Date Check
    IF NEW.type = 'Master' THEN
        IF EXISTS (SELECT 1 FROM Theses WHERE author_id=NEW.author_id AND type = 'Doctorate' AND submission_date<=NEW.submission_date) THEN
            RAISE EXCEPTION 'Master thesis cannot be published after the doctoral thesis submission date.';
        END IF;
    END IF;

    -- Doctoral Thesis Publication Date Check
    IF NEW.type = 'Doctorate' THEN
        IF EXISTS (SELECT 1 FROM Theses WHERE author_id=NEW.author_id AND type = 'Master' AND submission_date>=NEW.submission_date) THEN
            RAISE EXCEPTION 'Doctoral thesis cannot be published before the master thesis submission date.';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Activate the Trigger
CREATE TRIGGER thesis_publish_date_trigger
BEFORE INSERT OR UPDATE ON Theses
FOR EACH ROW EXECUTE FUNCTION check_thesis_publish_date();



-- Checks if author and supervisor/cosupervisor are the same person
-- Trigger Creation
CREATE OR REPLACE FUNCTION check_author_and_supervisors()
RETURNS TRIGGER AS $$
BEGIN
    -- Author-supervisor check
    IF NEW.author_id = NEW.supervisor OR NEW.author_id = NEW.cosupervisor THEN
        RAISE EXCEPTION 'Thesis author cannot be the same as the supervisor or co-supervisor.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Activate the Trigger
CREATE TRIGGER author_and_supervisors_trigger
BEFORE INSERT OR UPDATE ON Theses
FOR EACH ROW EXECUTE FUNCTION check_author_and_supervisors();




-- FILLING TABLES --
-- Persons
INSERT INTO Persons (title, NAME) VALUES
('Dr.', 'Ahmet Yılmaz'),
('Prof.', 'Mehmet Demir'),
('MSc.', 'Mustafa Baran'),
('Ph.D.', 'Emine Kılıç'),
('Dr.', 'Ali Özcan');

-- Universities
INSERT INTO Universities (NAME) VALUES
('University of California'),
('University of Oxford'),
('Massachusetts Institute of Technology'),
('Ege University'),
('Maltepe University');

-- Institutes
INSERT INTO Institutes (NAME, university_id) VALUES
('Science Institute', 1),
('Engineering Institute', 3),
('Business School', 2),
('Medical Institute', 4),
('Arts Institute', 5);


-- FILLING TABLES --
-- Theses
INSERT INTO Theses (title, abstract, author_id, year, TYPE, university_id, institute_id, num_pages, LANGUAGE, submission_date)
VALUES
('Exploring the Universe', 'This is an abstract about the universe...', 1, 2022, 'Master', 1, 1, 100, 'English', '2022-01-15'),
('Medical Breakthroughs', 'Research on breakthroughs in medicine...', 4, 2023, 'Doctorate', 4, 4, 150, 'Turkish', '2023-05-20'),
('Business Innovations', 'Innovative strategies for businesses...', 5, 2021, 'Master', 3, 3, 120, 'French', '2021-08-10'),
('Artistic Expressions', 'Expressing emotions through art...', 2, 2023, 'Proficiency in Art', 5, 5, 80, 'Turkish', '2023-11-30'),
('Environmental Sustainability', 'Sustainable practices for a better world...', 3, 2022, 'Master', 2, 2, 90, 'English', '2022-04-25');

-- Supervisors
INSERT INTO Supervisors (thesis_no, supervisor)
VALUES
(1, 2), -- Dr. Ahmet Yılmaz is the supervisor of the thesis '1'
(2, 1), -- Prof. Mehmet Demir is the supervisor of the thesis '2'
(3, 3), -- MSc. Mustafa Baran is the supervisor of the thesis '3'
(4, 4), -- Ph.D. Emine Kılıç is the supervisor off the thesis '4'
(5, 5); -- Dr. Ali Özcan is the supervisor of the thesis '5'

-- CoSupervisors
INSERT INTO CoSupervisors (thesis_no, cosupervisor)
VALUES
(1, 3), -- MSc. Mustafa Baran is the co-supervisor of the thesis '1'
(3, 2), -- Prof. Mehmet Demir is the co-supervisor of the thesis '3'
(4, 1); -- Dr. Ahmet Yılmaz is the co-supervisor of the thesis 4'

-- SubjectTopics
INSERT INTO SubjectTopics (topic_name) VALUES
('Astronomy and Space Sciences'), 
('Emergency Medicine'),
('Business Administration'),
('Fine Arts'),
('Environmental Engineering');

-- ThesisSubjectTopics
INSERT INTO ThesisSubjectTopics (thesis_no, topic_id) VALUES
(1, 1), -- Thesis '1' -> 'Astronomy and Space Sciences'
(2, 2), -- Thesis '2' -> 'Emergency Medicine'
(3, 3), -- Thesis '3' -> 'Business Administration'
(4, 4), -- Thesis '4' -> 'Fine Arts'
(5, 5); -- Thesis '5' -> 'Environmental Engineering'

-- Keywords
INSERT INTO Keywords (keyword) VALUES
('Space Exploration'),
('Medical Research'),
('Innovation'),
('Art'),
('Sustainability');

-- ThesisKeywords
INSERT INTO ThesisKeywords (thesis_no, keyword_id) VALUES
(1, 1), -- Thesis '1' -> 'Space Exploration'
(2, 2), -- Thesis '2' -> 'Medical Research'
(3, 3), -- Thesis '3' -> 'Innovation'
(4, 4), -- Thesis '4' -> 'Art'
(5, 5); -- Thesis '4' -> 'Sustainability'
