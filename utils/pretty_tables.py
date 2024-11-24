from utils.colouring import ConsoleColors


class PrettyTables:
    v_wall = 1
    h_wall = 1
    empty_space = ' '
    horizontal_line = '-'
    vertical_line = '|'

    def __init__(self, headers: list[str], table_data: dict.values, v_wall: int = None, h_wall: int = None,
                 empty_space: str = None, horizontal_line: str = None, vertical_line: str = None):
        if v_wall:
            self.v_wall = v_wall
        if h_wall:
            self.h_wall = h_wall
        if empty_space:
            self.empty_space = empty_space
        if horizontal_line:
            self.horizontal_line = horizontal_line
        if vertical_line:
            self.vertical_line = vertical_line

        self._rows_count = len(table_data) + 3 + self.h_wall
        self._headers = headers
        self._matrix = None
        self._table_data = table_data
        self._max_lens: list[int] = self.calculate_max_lens()
        self._columns_count = sum(self._max_lens) + (len(headers) + 1) * self.v_wall
        self.create_matrix()

    def calculate_max_lens(self) -> list[int]:
        lens = [0 for _ in range(len(self._headers))]
        for element in self._table_data:
            for i, value in enumerate(element.values()):
                lv = len(str(value))
                if lv > lens[i]:
                    lens[i] = lv
        for i, element in enumerate(self._headers):
            lv = len(str(element))
            if lv > lens[i]:
                lens[i] = lv
        return lens

    def create_matrix(self):
        rows: list[str] = [''.join(self.empty_space for _ in range(self._columns_count)) for row in
                           range(self._rows_count)]
        self._paint_borders(rows)
        self._paint_headers(rows)
        self._paint_data(rows)

        self._matrix = rows

    def _paint_borders(self, rows: list[str]):
        need_horizontal_filling = [0, -1, *[row for row in range(2, 2 + self.h_wall)]]
        for row in need_horizontal_filling:
            if row not in [0, -1]:
                rows[row] = '|' + self.string_filling(rows[row])[1:-1] + '|'
            else:
                rows[row] = self.string_filling(rows[row])

    def string_filling(self, string: str) -> str:
        return string.replace(self.empty_space, '-')

    def _paint_headers(self, rows: list[str]):
        headers_line = rows[1]
        rows[1] = self._paint_string(headers_line, self._headers)

    def _paint_data(self, rows):
        first_str = 2 + self.h_wall
        last_str = first_str + len(self._table_data)
        data_i = 0
        data = list(self._table_data)
        for i, row in enumerate(rows):
            if i in range(first_str, last_str):
                rows[i] = self._paint_string(row, data[data_i].values())
                data_i += 1

    def _paint_string(self, row: str, data: list[str]) -> str:
        start = 1
        for i, header in enumerate(data):
            row = row[:start] + str(header) + row[start + len(str(header)):start + self._max_lens[
                i]] + '|' * self.v_wall + row[start + self._max_lens[i] + 1:]
            start += self.v_wall + self._max_lens[i]
        row = '|' + row[1:]
        return row

    def _set_colors(self, row: str) -> str:
        row = ''.join(map(lambda s: ConsoleColors.colour_background(ConsoleColors.colour_bright_text(
            s, 'BLACK'), 'BLACK'), [letter for letter in row]))
        return row.replace(
            self.vertical_line, ConsoleColors.colour_bright_text(self.vertical_line, 'GREEN')
        ).replace(
            self.horizontal_line, ConsoleColors.colour_bright_text(self.horizontal_line, 'GREEN')
        )

    def get_pretty_table(self):
        table = "\n"
        for row in self._matrix:
            table += f'{self._set_colors(row)}\n'

        return table
