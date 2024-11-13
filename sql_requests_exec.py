import psycopg2

# Параметри підключення до БД
conn = psycopg2.connect(
    dbname="clinic_db", user="admin", password="password", host="localhost", port="8054"
)
cur = conn.cursor()

cur.execute("""
    SELECT * FROM Patients WHERE birth_year > 1998 ORDER BY last_name;
""")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.execute("""
    SELECT category, COUNT(*) FROM Patients GROUP BY category;
""")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.execute("""
    SELECT patient_id, SUM(treatment_cost_per_day * stay_duration * (1 - discount_percentage / 100)) 
    FROM Hospitalizations GROUP BY patient_id;
""")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.execute("""
    SELECT * FROM Hospitalizations WHERE doctor_id IN (SELECT doctor_id FROM Doctors WHERE specialization = %s);
""", ('Терапевт',))
rows = cur.fetchall()
for row in rows:
    print(row)

cur.execute("""
    SELECT doctor_id, COUNT(*) FROM Hospitalizations GROUP BY doctor_id;
""")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.execute("""
    SELECT specialization, category, COUNT(*) FROM Doctors 
    JOIN Hospitalizations ON Doctors.doctor_id = Hospitalizations.doctor_id
    JOIN Patients ON Hospitalizations.patient_id = Patients.patient_id
    GROUP BY specialization, category;
""")
rows = cur.fetchall()
for row in rows:
    print(row)


conn.commit()
cur.close()
conn.close()