"""Выполняет sql/checks_duckdb.sql и сохраняет вывод в checks_output.txt"""
import duckdb
from pathlib import Path

con = duckdb.connect("retail.duckdb", read_only=True)
sql = Path("sql/checks_duckdb.sql").read_text(encoding="utf-8")

# Разделяем на отдельные запросы по ";"
queries = [q.strip() for q in sql.split(";") if q.strip()]

output_lines = []
output_lines.append("РЕЗУЛЬТАТЫ ПРОВЕРОК ВИТРИНЫ")

for i, query in enumerate(queries, 1):
    output_lines.append(f"\n Проверка {i} ")
    try:
        result = con.execute(query).fetchdf()
        output_lines.append(result.to_string(index=False))
    except Exception as e:
        output_lines.append(f"Ошибка: {e}")

con.close()

output_text = "\n".join(output_lines)
print(output_text)

# Сохраняем в файл
Path("checks_output.txt").write_text(output_text, encoding="utf-8")
print("Вывод сохранён в checks_output.txt")