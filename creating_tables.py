import psycopg2

# Параметри підключення до БД
conn = psycopg2.connect(
    dbname="clinic_db", user="admin", password="password", host="localhost", port="8054"
)
cur = conn.cursor()

# Створення таблиць
cur.execute("""
    CREATE TABLE IF NOT EXISTS Patients (
        patient_id SERIAL PRIMARY KEY,
        last_name VARCHAR(255),
        first_name VARCHAR(255),
        patronymic VARCHAR(255),
        address TEXT,
        phone VARCHAR(20),
        birth_year INT,
        category VARCHAR(20)
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Doctors (
        doctor_id SERIAL PRIMARY KEY,
        last_name VARCHAR(255),
        first_name VARCHAR(255),
        patronymic VARCHAR(255),
        specialization VARCHAR(50),
        work_experience INT
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Hospitalizations (
        hospitalization_id SERIAL PRIMARY KEY,
        patient_id INT REFERENCES Patients(patient_id),
        admission_date DATE,
        stay_duration INT,
        treatment_cost_per_day DECIMAL(10, 2),
        discount_percentage DECIMAL(5, 2),
        doctor_id INT,
        FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
        FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
    );
""")

# Вставка даних у таблицю лікарів
cur.execute("""
    INSERT INTO Doctors (last_name, first_name, patronymic, specialization, work_experience)
    VALUES
    ('Іванов', 'Іван', 'Іванович', 'Терапевт', 10),
    ('Петров', 'Петро', 'Петрович', 'ЛОР', 5),
    ('Сидоров', 'Сидор', 'Сидорович', 'Хірург', 8);
""")

# Вставка даних у таблицю пацієнтів
cur.execute("""
    INSERT INTO Patients (last_name, first_name, patronymic, address, phone, birth_year, category)
    VALUES
    ('Андріїв', 'Андрій', 'Андрійович', 'Київ, вул. Лесі Українки, 1', '0991234567', 1999, 'Дитяча'),
    ('Боровик', 'Сергій', 'Вікторович', 'Київ, вул. Шевченка, 5', '0679876543', 1985, 'Доросла');
""")

# Вставка даних у таблицю стаціонарних пацієнтів
cur.execute("""
    INSERT INTO Hospitalizations (patient_id, admission_date, stay_duration, treatment_cost_per_day, discount_percentage, doctor_id)
    VALUES
    (1, '2024-11-01', 5, 1000.00, 10, 1),
    (2, '2024-11-02', 3, 1200.00, 5, 2);
""")


conn.commit()
cur.close()
conn.close()
