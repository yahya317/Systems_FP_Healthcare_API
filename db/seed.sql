DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    blood_type VARCHAR(5),
    medical_condition VARCHAR(100),
    date_of_admission DATE,
    doctor VARCHAR(100),
    hospital VARCHAR(100),
    insurance_provider VARCHAR(100),
    billing_amount FLOAT,
    room_number INT,
    admission_type VARCHAR(50),
    discharge_date DATE,
    medication VARCHAR(100),
    test_results VARCHAR(100)
);

COPY patients(name, age, gender, blood_type, medical_condition, date_of_admission, doctor, hospital, insurance_provider, billing_amount, room_number, admission_type, discharge_date, medication, test_results)
FROM '/data/healthcare_dataset.csv'
DELIMITER ','
CSV HEADER;
