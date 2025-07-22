import sqlite3

conn = sqlite3.connect('fabrica_chocolate.db')

cursor = conn.cursor()

# Consulta 1: Tribos com mais de 1 OompaLoompa
cursor.execute(
    """
    SELECT 
        TRIBO,
        COUNT(*) as Total_OompaLoompas
    FROM OompaLoompa
    GROUP BY TRIBO
    HAVING COUNT(*) > 1
    ORDER BY Total_OompaLoompas DESC;
    """
)

result = cursor.fetchall()

print("\nTribos com mais de 1 OompaLoompa:")
for row in result:
    print(f'Tribo: {row[0]}, Total de OompaLoompas: {row[1]}')

conn.close()