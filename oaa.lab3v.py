class Table:
    def __init__(self, name):
        self.name = name
        self.columns = []
        self.rows = []
        self.indexes = {}

    def add_column(self, name, index=False):
        self.columns.append({"назва": name})
        if index:
            self.indexes[name] = {}

    def insert(self, values):
        if len(values) != len(self.columns):
            return f"Помилка! Кількість значень не відповідає кількості стовпців!"

        try:
            values = [int(value) for value in values]
        except ValueError:
            return f"Помилка! Усі значення повинні бути цілочисельними!"

        row_idx = len(self.rows)
        self.rows.append(values)

        for col_idx, value in enumerate(values):
            column_name = self.columns[col_idx]["назва"]
            if column_name in self.indexes:
                if value not in self.indexes[column_name]:
                    self.indexes[column_name][value] = []
                self.indexes[column_name][value].append(row_idx)

        return f"1 рядок додано до таблиці {self.name}."

    def __str__(self):
        return f"Таблиця {self.name} створена зі стовпцями: " + ", ".join([col["назва"] for col in self.columns])

    def display(self):
        if not self.rows:
            return "Таблиця порожня."

        column_widths = [len(col["назва"]) for col in self.columns]
        for row in self.rows:
            for i, value in enumerate(row):
                column_widths[i] = max(column_widths[i], len(str(value)))

        header = "| " + " | ".join([col["назва"].ljust(column_widths[i]) for i, col in enumerate(self.columns)]) + " |"
        separator = "+" + "+".join(["-" * (width + 2) for width in column_widths]) + "+"
        formatted_rows = "\n".join(["| " + " | ".join([str(value).ljust(column_widths[i]) for i, value in enumerate(row)]) + " |" for row in self.rows])
        return f"\n{separator}\n{header}\n{separator}\n{formatted_rows}\n{separator}"

    def select(self, select_clause, where_clause=None, group_by_clause=None):
        column_names = [col["назва"] for col in self.columns]

        if select_clause.strip() == "":
            select_columns = column_names
        else:
            select_columns = [col.strip() for col in select_clause.split(",")]

        filtered_rows = self.rows
        if where_clause:
            try:
                operator = None
                if "=" in where_clause:
                    operator = "="
                elif ">" in where_clause:
                    operator = ">"
                elif "<" in where_clause:
                    operator = "<"
                if operator:
                    where_column, where_value = where_clause.split(operator)
                    where_column, where_value = where_column.strip(), float(where_value.strip())
                    if where_column not in column_names:
                        return print(f"Помилка! Стовпець '{where_column}' не знайдено.")

                    col_idx = column_names.index(where_column)

                    if operator == "=" and where_column in self.indexes:
                        if where_value in self.indexes[where_column]:
                            row_indices = self.indexes[where_column][where_value]
                            filtered_rows = [self.rows[idx] for idx in row_indices]
                        else:
                            filtered_rows = []
                    else:
                        if operator == "=":
                            filtered_rows = [row for row in filtered_rows if row[col_idx] == where_value]
                        elif operator == ">":
                            filtered_rows = [row for row in filtered_rows if row[col_idx] > where_value]
                        elif operator == "<":
                            filtered_rows = [row for row in filtered_rows if row[col_idx] < where_value]
            except Exception:
                return print(f"Помилка у WHERE")

        if group_by_clause:
            try:
                group_by_columns = [col.strip() for col in group_by_clause.split(",")]

                for col in group_by_columns:
                    if col not in column_names:
                        return print(f"Помилка! Стовпець '{col}' не знайдено.")

                grouped_data = {}
                for row in filtered_rows:
                    group_key = tuple(row[column_names.index(col)] for col in group_by_columns)
                    if group_key not in grouped_data:
                        grouped_data[group_key] = []
                    grouped_data[group_key].append(row)

                result = []
                for group_key, rows in grouped_data.items():
                    aggregated_row = list(group_key)
                    for col in select_columns:
                        col = col.strip()
                        if col.startswith("COUNT(") and col.endswith(")"):
                            aggregated_row.append(len(rows))
                        elif col.startswith("MAX(") and col.endswith(")"):
                            col_name = col[4:-1].strip()
                            if col_name not in column_names:
                                return print(f"Помилка! Стовпець '{col_name}' не знайдено.")
                            col_idx = column_names.index(col_name)
                            aggregated_row.append(max(row[col_idx] for row in rows))
                        elif col.startswith("AVG(") and col.endswith(")"):
                            col_name = col[4:-1].strip()
                            if col_name not in column_names:
                                return print(f"Помилка! Стовпець '{col_name}' не знайдено.")
                            col_idx = column_names.index(col_name)
                            aggregated_row.append(sum(row[col_idx] for row in rows) / len(rows))
                        elif col in group_by_columns:
                            continue
                        else:
                            return print(f"Помилка! '{col}' не є підтримуваною функцією чи стовпцем у SELECT.")
                    result.append(aggregated_row)
                result = sorted(result, key=lambda row: tuple(row[group_by_columns.index(col)] for col in group_by_columns))
                return result

            except Exception:
                return print(f"Помилка у GROUP_BY")

        try:
            result = [[row[column_names.index(col)] for col in select_columns] for row in filtered_rows]
        except ValueError:
            return print(f"Помилка у SELECT")
        return result

    def show_selection(self, select_columns, where_clause=None, group_by_clause=None):
        if select_columns == "":
            select_columns = ','.join([col["назва"] for col in self.columns])
        else:
            select_columns = group_by_clause + "," + select_columns

        selected_data = self.select(select_columns, where_clause, group_by_clause)
        if not selected_data:
            return "Немає результатів для вибірки."

        column_names = [col.strip() for col in select_columns.split(",")]
        column_widths = [len(name) for name in column_names]
        for row in selected_data:
            for i, value in enumerate(row):
                column_widths[i] = max(column_widths[i], len(str(value)))

        header = "| " + " | ".join([name.ljust(column_widths[i]) for i, name in enumerate(column_names)]) + " |"
        separator = "+" + "+".join(["-" * (width + 2) for width in column_widths]) + "+"
        rows = "\n".join(["| " + " | ".join([str(value).ljust(column_widths[i]) for i, value in enumerate(row)]) + " |" for row in selected_data])
        return f"\n{separator}\n{header}\n{separator}\n{rows}\n{separator}"



class Database:
    def __init__(self):
        self.tables = {}

    def execute(self, command):
        if ";" in command:
            command = command.split(";", 1)[0].strip()

        if command.upper().startswith("CREATE"):
            return self.create_table(command)
        elif command.upper().startswith("INSERT"):
            return self.insert_into_table(command)
        elif command.upper().startswith("SHOW"):
            return self.show_table(command)
        elif command.upper().startswith("SELECT"):
            return self.select_from_table(command)
        else:
            return "Помилка! Такої команди немає, спробуйте ще раз."

    def create_table(self, command):
        try:
            parts = command[7:].split("(")
            table_name = parts[0].strip()
            if not table_name[0].isalpha():
                return f"Помилка! Назва таблиці повинна починатися з літери."

            column_definitions = parts[1].replace(")", "").split(",")
            if table_name in self.tables:
                return f"Помилка! Таблиця '{table_name}' вже існує."

            table = Table(table_name)
            for column in column_definitions:
                column = column.strip()
                if "INDEXED" in column.upper():
                    column_name = column.replace("INDEXED", "").strip()
                    table.add_column(column_name, index=True)
                else:
                    table.add_column(column.strip())
            self.tables[table_name] = table
            return f"\nТаблиця {table_name} створена."

        except Exception:
            return f"Помилка! Неправильна команда CREATE."

    def insert_into_table(self, command):
        try:
            if "INTO" in command.upper():
                parts = command[12:].split("(")
            else:
                parts = command[7:].split("(")
            table_name = parts[0].strip()

            if table_name not in self.tables:
                return f"Помилка! Таблиця '{table_name}' не знайдена."

            values = parts[1].replace(")", "").split(",")
            values = [value.strip() for value in values]
            return self.tables[table_name].insert(values)

        except Exception:
            return f"Помилка! Неправильна команда INSERT."

    def show_table(self, command):
        try:
            table_name = command[5:].strip()
            if table_name not in self.tables:
                return f"Помилка! Таблиця '{table_name}' не знайдена."

            return self.tables[table_name].display()

        except Exception:
            return f"Помилка! Неправильна команда SHOW."

    def select_from_table(self, command):
        try:
            command = command.lower()
            parts = command[7:].split("from")

            if len(parts) < 2:
                return "Помилка! Неправильна команда SELECT."

            select_clause = parts[0].strip()
            if select_clause:
                clauses = [clause.strip() for clause in select_clause.split(",")]
                processed_clauses = []
                for clause in clauses:
                    if clause.lower().startswith("count("):
                        clause = "COUNT" + clause[5:]
                    elif clause.lower().startswith("max("):
                        clause = "MAX" + clause[3:]
                    elif clause.lower().startswith("avg("):
                        clause = "AVG" + clause[3:]
                    processed_clauses.append(clause.strip())
                select_clause = ", ".join(processed_clauses)
            rest = parts[1].strip().lower()
            table_name, where_clause, group_by_clause = None, None, None

            if "where" in rest:
                table_name, rest = rest.split("where", 1)
                table_name = table_name.strip()
                rest = rest.strip()

                if "group_by" in rest:
                    where_clause, group_by_clause = rest.split("group_by", 1)
                    where_clause = where_clause.strip()
                    group_by_clause = group_by_clause.strip()
                else:
                    where_clause = rest.strip()

            elif "group_by" in rest:
                table_name, group_by_clause = rest.split("group_by", 1)
                table_name = table_name.strip()
                group_by_clause = group_by_clause.strip()

            else:
                table_name = rest.strip()

            if table_name not in self.tables:
                return f"Помилка! Таблиця '{table_name}' не знайдена."

            return self.tables[table_name].show_selection(select_clause, where_clause, group_by_clause)

        except Exception:
            return f"Помилка! Неправильна команда SELECT."

    def show_all_tables(self):
        if not self.tables:
            return "Немає створених таблиць."

        return "\n".join([str(table) for table in self.tables.values()])

    def read_multiline_command(self):
        lines = []
        while True:
            line = input().strip()
            if ";" in line:
                line = line.split(";", 1)[0] + ";"
                lines.append(line)
                break
            else:
                lines.append(line)
        return " ".join(lines).strip()



"""import random
import time

db = Database()

db.execute("CREATE boys (id, age, height INDEXED, weight);")

for i in range(1, 100000):
    age = random.randint(18, 45)
    height = random.randint(155, 195)
    weight = random.randint(55, 95)
    db.execute(f"INSERT INTO boys ({i}, {age}, {height}, {weight});")

start_time = time.time()
result1 = db.execute("SELECT FROM boys WHERE height = 170;")
end_time = time.time()
print(f"Час виконання з індексом: {end_time - start_time} секунд")


start_time = time.time()
result2 = db.execute("SELECT FROM boys WHERE weight = 70;")
end_time = time.time()
print(f"Час виконання без індексу: {end_time - start_time} секунд")

#print(db.execute("SHOW boys;"))"""



def main():
    db = Database()
    while True:
        command = db.read_multiline_command()
        if not command:
            continue
        if command.lower() == "show all tables;":
            print(db.show_all_tables())
        elif command.lower() == "help;":
            print("CREATE table_name (column_name *[INDEXED] [, ...]); - команда, яка створює таблицю зі стовпцями; \n")
            print("INSERT [INTO] table_name (N [, ...]); - команда, яка додає рядки у відповідну таблицю; \n")
            print("SHOW table_name; - команда, яка демонструє вигляд таблиці; \n")
            print("SHOW ALL TABLES; - команда, яка виводить список створених таблиць; \n")
            print("SELECT [agg_function(agg_column) [, ... ]] FROM table_name [WHERE condition] [GROUP_BY column_name [, ...] ]; - команда для вибірки даних із таблиці; \n")
            print(">>> COUNT(column) - кількість значень в групі, незалежно від того, до якого стовпця застосовується; \n")
            print(">>> MAX(column) - максимальне значення стовпця column в межах групи; \n")
            print(">>> AVG(column) - середнє значення стовпця column в межах групи. \n")
        else:
            result = db.execute(command)
            print(result)

if __name__ == "__main__":
    main()
