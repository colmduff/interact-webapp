DROP TABLE IF EXISTS 'users';
DROP TABLE IF EXISTS 'survey_questions';
DROP TABLE IF EXISTS 'survey_results';

CREATE TABLE 'users' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    'username' TEXT NOT NULL,
    'hash' TEXT NOT NULL,
    'survey_complete' INTEGER DEFAULT 0);



CREATE TABLE 'survey_questions' (
    'q_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    'question' TEXT,
    'response1' TEXT,
    'response2' TEXT,
    'response3' TEXT,
    'response4' TEXT,
    'response5' TEXT);

INSERT INTO survey_questions (question, response1, response2, response3, response4, response5)
VALUES
('gender', 'Female', 'Male', 'Transmale', 'Transfemale', 'Prefer not to say'),
('age', '14-17', '18-25', '26-35', '35-55', 'over 55'),
('education', 'First level', 'Second level', 'Degree', 'Masters', 'Doctorate'),
('climate_k_rating', 'None', 'Basic', 'Average', 'Above average', 'Expert'),
('climate_info_source', 'Education system', 'Online news media', 'Online research', 'Social media networks', 'Print media'),
('climate_causes', 'Anthropogenic activity', 'Natural cycle','Not real', 'Volcanic activity', 'Solar activity'),
('anxiety', 'No impact', 'A little worried', 'Somewhat worried', 'Relatively anxious', 'Very anxious'),
('personal', 'Not at all', 'A little', 'Somewhat', 'A lot of input', 'Constant input'),
('government_action', 'Terrible', 'Insufficent', 'OK', 'Good', 'Great'),
('politics', 'Left', 'Centre left', 'Centre', 'Centre right', 'Right');


CREATE TABLE 'survey_results' (

    'survey_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    'user_id' INTEGER NOT NULL,
    'gender' TEXT NOT NULL,
    'age' TEXT NOT NULL,
    'education' TEXT NOT NULL,
    'climate_k_rating' TEXT NOT NULL,
    'climate_info_source' TEXT NOT NULL,
    'climate_causes' TEXT NOT NULL,
    'anxiety' TEXT NOT NULL,
    'personal' TEXT NOT NULL,
    'government_action' TEXT NOT NULL,
    'politics' TEXT NOT NULL,
    'country' TEXT NOT NULL,
    'date' TEXT NOT NULL);