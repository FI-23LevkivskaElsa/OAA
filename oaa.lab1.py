class Table:
    def __init__(self, name):
        self.name = name
        self.columns = []
        self.rows = []

    def add_column(self, name, indexed=False):
        self.columns.append({"назва": name, "індекс": indexed})

    def insert(self, values):
        if len(values) != len(self.columns):
            return f"Помилка: кількість значень не відповідає кількості стовпців!"
        for value in values:
            try:
                int(value)
            except ValueError:
                return f"Помилка: значення '{value}' не є  цілим числом"

        self.rows.append([int(value) for value in values])
        return f"1 рядок додано до таблиці {self.name}."

    def __str__(self):
        return f"Таблиця {self.name} створена зі стовпцями: " + ", ".join([f"{col['назва']}{' (ІНДЕКС)' if col['індекс'] else ''}" for col in self.columns])

    def display(self):
        column_widths = [len(col['назва']) for col in self.columns]
        for row in self.rows:
            for i, value in enumerate(row):
                column_widths[i] = max(column_widths[i], len(str(value)))

        header = " | ".join([col['назва'].ljust(column_widths[i]) for i, col in enumerate(self.columns)])
        separator = "-" * len(header)

        formatted_rows = []
        for row in self.rows:
            formatted_row = " | ".join([str(value).ljust(column_widths[i]) for i, value in enumerate(row)])
            formatted_rows.append(formatted_row)

        table_str = f"{header}\n{separator}\n" + "\n".join(formatted_rows)
        return table_str if formatted_rows else "Таблиця порожня."

    @classmethod
    def create_table_interactive(cls):
        table_name = input("Введіть назву таблички: ")
        table = cls(table_name)
        while True:
            column_input = input("Введіть назву стовпця (або напишіть 'стоп', щоб завершити): ")
            if column_input.lower() == 'стоп':
                break
            index_input = input(f"Чи треба стовпець '{column_input}' проіндексувати? (так/ні): ").strip().lower()
            indexed = index_input == 'так'
            table.add_column(column_input, indexed)
        print(table)
        while True:
            insert_input = input("Введіть дані для вставки через кому (або напишіть 'стоп', щоб завершити): ")
            if insert_input.lower() == 'стоп':
                break
            values = [val.strip() for val in insert_input.split(",")]
            result = table.insert(values)
            print(result)
        print("\nТаблиця після вставки даних:")
        print(table.display())

Table.create_table_interactive()
