import pandas as pd
import mysql.connector

# Step 1: Load CSV
df = pd.read_csv('/home/jayashree/quiz/Home/quesgen/question_fine_turned.csv', encoding='iso-8859-1')

# Step 2: Connect to MySQL
conn = mysql.connector.connect(
    host='10.15.1.2',
    user='quiz_application',
    password='quiz123',
    database='quiz_db'
)
cursor = conn.cursor()

# Step 3: Insert rows
for _, row in df.iterrows():
    query = """
        INSERT INTO questions_fine_tuned (question_text, bloom_level,answer)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (row['question_text'], row['bloom_level'], row['answer']))

conn.commit()
cursor.close()
conn.close()

print("? CSV data inserted successfully.")
