class Table:
    def __init__(self, name):
        self.name = name
        self.columns = []
        self.rows = []

    def add_column(self, name, indexed=False):
        self.columns.append({"назва": name, "індекс": indexed})

    def insert(self, values):
        if len(values) != len(self.columns):
            return f"Помилка! Кількість значень не відповідає кількості стовпців!"
        for value in values:
            try:
                float(value)
            except ValueError:
                return f"Помилка! Значення '{value}' не є числом!"
        self.rows.append(values)
        return f"1 рядок додано до таблиці {self.name}."

    def __str__(self):
        return f"Таблиця {self.name} створена зі стовпцями: " + ", ".join([f"{col['назва']}{' INDEXED' if col['індекс'] else ''}" for col in self.columns])

    def display(self):
        if not self.rows:
            return "Таблиця порожня."
        column_widths = [len(col["назва"]) for col in self.columns]
        for row in self.rows:
            for i, value in enumerate(row):
                column_widths[i] = max(column_widths[i], len(str(value)))
        header = "| "+" | ".join([col["назва"].ljust(column_widths[i]) for i, col in enumerate(self.columns)]) + " |"
        separator = "+" + "+".join(["-" * (width + 2) for width in column_widths]) + "+"
        formatted_rows = []
        for row in self.rows:
            formatted_row = "| "+" | ".join([str(value).ljust(column_widths[i]) for i, value in enumerate(row)]) + " |"
            formatted_rows.append(formatted_row)
        table_str = f"{separator}\n{header}\n{separator}\n" + "\n".join(formatted_rows) + f"\n{separator}"
        return table_str


class Database:
    def __init__(self):
        self.tables = {}

    def execute(self, command):
        command = command.strip()
        if not command.endswith(";"):
            return "Помилка! Команда повинна закінчуватись на ';'."
        command = command[:-1].strip()
        if command.upper().startswith("CREATE"):
            return self.create_table(command)
        elif command.upper().startswith("INSERT"):
            return self.insert_into_table(command)
        elif command.upper().startswith("SHOW"):
            return self.show_table(command)
        else:
            return "Помилка! Такої команди немає, спробуйте ще раз."

    def create_table(self, command):
        try:
            parts = command[7:].split("(")
            table_name = parts[0].strip()
            column_definitions = parts[1].replace(")", "").split(",")
            if table_name in self.tables:
                return f"Помилка! Таблиця '{table_name}' вже існує."
            table = Table(table_name)
            for column in column_definitions:
                column = column.strip()
                if column.endswith("INDEXED"):
                    table.add_column(column.replace(" INDEXED", "").strip(), indexed=True)
                else:
                    table.add_column(column)
            self.tables[table_name] = table
            return f"Таблиця {table_name} створена."
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

    def show_all_tables(self):
        if not self.tables:
            return "Немає створених таблиць."
        return "\n".join([str(table) for table in self.tables.values()])


def main():
    db = Database()
    while True:
        command = input().strip()
        if command.lower() == "show all tables;":
            print(db.show_all_tables())
        elif command.lower() == "help;":
            print("CREATE table_name (column_name *[INDEXED] [, ...]); - команда, яка створює таблицю зі стовпцями; \n")
            print("INSERT [INTO] table_name (N [, ...]); - команда, яка додає рядки у відповідну таблицю; \n")
            print("SHOW table_name; - команда, яка демонструє вигляд таблиці; \n")
            print("SHOW ALL TABLES; - команда, яка виводить список створених таблиць; \n")
        else:
            result = db.execute(command)
            print(result)

if __name__ == "__main__":
    main()
