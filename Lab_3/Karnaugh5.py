from KarnaughTemplate import KarnaughTemplate, BooleanExpression


class Karnaugh5(KarnaughTemplate):
    def __init__(self, exp: BooleanExpression, form_to_minimize: str):
        self.header_line = \
            [
                ['0', '0', '0', '0', '1', '1', '1', '1'],
                ['0', '0', '1', '1', '1', '1', '0', '0'],
                ['0', '1', '1', '0', '0', '1', '1', '0']
            ]
        self.header_column = \
            [
                ['0', '0', '1', '1'],
                ['0', '1', '1', '0']
            ]
        super().__init__(exp, form_to_minimize)
        self.map: list[list[int]] = self.build_map()
        self.map_left_side: list[list[int]] = []
        self.map_right_side: list[list[int]] = []
        self.map_left_side, self.map_right_side = self.build_sides()

    def build_map(self) -> list[list[int]]:
        for i in range(len(self.header_column[0])):
            for j in range(len(self.header_line[0])):
                self.index_chain_for_iteration.append(
                    self.to_decimal_form(self.header_column[0][i] + self.header_column[1][i]
                                         + self.header_line[0][j] + self.header_line[1][j] + self.header_line[2][j]))
        table: list[list[int]] = []
        counter = 0
        for i in range(len(self.header_column[0])):
            table.append([])
            for j in range(len(self.header_line[0])):
                table[i].append(self.result_values[self.index_chain_for_iteration[counter]])
                counter += 1
        return table

    def check_field_validity(self, field: list[tuple]) -> bool:
        # check if all cells has same value
        if not field:
            return False
        first_value = self.map[field[0][0]][field[0][1]]
        return all(self.map[i][j] == first_value for i, j in field)

    def build_sides(self) -> (list[list[int]], list[list[int]]):
        right_half: list[list[int]] = []
        left_half: list[list[int]] = []
        for i in self.map:
            left_half.append([i[j] for j in range(4)])
            right_half.append([i[j] for j in range(4, len(i))])
        return left_half, right_half

    def form_final_normal_form_fields(self) -> list[list[tuple]]:
        used_indexes: list[tuple] = []
        fields: list[list[tuple]] = []
        value: int = 1 if self.form_to_minimize == 'SDNF' else 0
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if not (i, j) in used_indexes and self.map[i][j] == value:
                    half = self.map_left_side if j < 4 else self.map_right_side
                    side: str = 'left' if j < 4 else 'right'
                    field = self.form_field(half, (i, j % 4), value, side)
                    for index in field:
                        if index not in used_indexes:
                            used_indexes.append(index)
                    fields.append(field)
        return fields

    def negate_map_values(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                self.map[i][j] = 1 - self.map[i][j]

    def form_field(self, half: list[list[int]], initial_index: tuple, value: int, side: str) -> list[tuple]:
        one_half_field: list[tuple] = self.form_field_in_half(half, initial_index, value)
        fixed_one_half_field: list[tuple] = []
        if side == 'right':
            for i in one_half_field:
                fixed_one_half_field.append((i[0], i[1] + len(half)))
        else:
            fixed_one_half_field = one_half_field
        other_half: list[list[int]] = self.map_right_side if side == 'left' else self.map_left_side
        total_field: list[tuple] = self.find_equivalence_in_other_half(other_half, fixed_one_half_field, value)
        return total_field

    def form_field_in_half(self, half: list[list[int]], initial_index: tuple, value: int) -> list[tuple]:
        possible_way_to_spread: dict = {
            'right': True,
            'left': True,
            'top': True,
            'down': True
        }
        degrees = [1, 2, 4, 8]
        field: list[tuple] = [initial_index]
        while possible_way_to_spread['top']:
            last: tuple = field[len(field) - 1]
            if possible_way_to_spread['right']:
                if last[1] <= len(half[0]) - 2:
                    if half[last[0]][last[1] + 1] == value and (last[0], last[1] + 1) not in field:
                        field.append((last[0], last[1] + 1))
                    else:
                        if len(field) not in degrees:
                            field = self.cut_cells_list(field, True)
                        possible_way_to_spread['right'] = False
                else:
                    if half[last[0]][0] == value and (last[0], 0) not in field:
                        field.append((last[0], 0))
                    else:
                        if len(field) not in degrees:
                            field = self.cut_cells_list(field, True)
                        possible_way_to_spread['right'] = False
            elif possible_way_to_spread['left']:
                if last[1] >= 1:
                    if half[last[0]][last[1] - 1] == value and (last[0], last[1] - 1) not in field:
                        field.insert(0, (last[0], last[1] - 1))
                    else:
                        if len(field) not in degrees:
                            field = self.cut_cells_list(field, False)
                        possible_way_to_spread['left'] = False
                else:
                    if (half[last[0]][len(half[0]) - 1] == value and (last[0], len(half[0]) - 1)
                            not in field):
                        field.insert(0, (last[0], len(half[0]) - 1))
                    else:
                        if len(field) not in degrees:
                            field = self.cut_cells_list(field, False)
                        possible_way_to_spread['left'] = False
            elif possible_way_to_spread['down']:
                new_indexes = self.possibility_to_go_down(half, field, value)
                field += new_indexes
                if len(field) not in degrees:
                    field = self.cut_cells_list(field, True)
                possible_way_to_spread['down'] = False
            elif possible_way_to_spread['top']:
                new_indexes = self.possibility_to_go_top(half, field, value)
                field += new_indexes
                if len(field) not in degrees:
                    field = self.cut_cells_list(field, True)
                possible_way_to_spread['top'] = False
        self.calculate_field_perimeter(field)
        self.expand_field(field, 1)
        return field

    def get_variables_after_merge(self) -> list[list[str]]:
        fields: list[list[tuple]] = self.form_final_normal_form_fields()
        if self.form_to_minimize == 'SDNF':
            value = '1'
        else:
            value = '0'
        variables: list[list[str]] = []
        for i in range(len(fields)):
            initial_values: list[str] = [self.header_column[0][fields[i][0][0]], self.header_column[1][fields[i][0][0]],
                                         self.header_line[0][fields[i][0][1]], self.header_line[1][fields[i][0][1]],
                                         self.header_line[2][fields[i][0][1]]]
            different: list[bool] = [False] * len(self.variables)
            self.expand_field(fields[i], int(value))
            for j in fields[i]:
                self.check_field_validity(fields[i])
                if self.header_column[0][j[0]] != initial_values[0]:
                    different[0] = True
                elif self.header_column[1][j[0]] != initial_values[1]:
                    different[1] = True
                elif self.header_line[0][j[1]] != initial_values[2]:
                    different[2] = True
                elif self.header_line[1][j[1]] != initial_values[3]:
                    different[3] = True
                elif self.header_line[2][j[1]] != initial_values[4]:
                    different[4] = True

            final_variables_from_field: list[str] = []
            for j in range(len(different)):
                if not different[j]:
                    final_variables_from_field.append(self.variables[j] if initial_values[j] == value
                                                      else '(!' + self.variables[j] + ')')
                self.calculate_field_perimeter(fields[i])
            variables.append(final_variables_from_field)
        return variables

    def possibility_to_go_top(self, half: list[list[int]], field: list[tuple], value: int) -> list[tuple]:
        cells_in_one_row: list[tuple] = []
        row_index_from_first_cell: int = field[0][0]
        for i in range(len(field)):
            if row_index_from_first_cell != field[i][0]:
                break
            cells_in_one_row.append(field[i])
        next_row_to_check = len(half) - 1 if cells_in_one_row[0][0] == 0 else cells_in_one_row[0][0] - 1
        go_status = True
        possible_to_go_cells = []
        while go_status:
            for i in range(len(cells_in_one_row)):
                self.expand_field(field, value)
                if (half[next_row_to_check][cells_in_one_row[i][1]] != value or
                        (next_row_to_check, cells_in_one_row[i][1]) in possible_to_go_cells or
                        (next_row_to_check, cells_in_one_row[i][1]) in field):
                    go_status = False
                    self.check_field_validity(field)
                    break
            if go_status:
                for i in range(len(cells_in_one_row)):
                    possible_to_go_cells.append((next_row_to_check, cells_in_one_row[i][1]))
                next_row_to_check = len(half) - 1 if next_row_to_check == 0 else next_row_to_check - 1
        return possible_to_go_cells

    def possibility_to_go_down(self, half: list[list[int]], field: list[tuple], value: int) -> (bool, list[tuple]):
        cells_in_one_row: list[tuple] = []
        row_index_from_last_cell: int = field[len(field) - 1][0]
        for i in range(len(field) - 1, -1, -1):
            if row_index_from_last_cell != field[i][0]:
                break
            cells_in_one_row.append(field[i])
        next_row_to_check: int = 0 if cells_in_one_row[0][0] == len(half) - 1 else cells_in_one_row[0][0] + 1
        go_status: bool = True
        possible_to_go_cells: list[tuple] = []
        while go_status:
            for i in range(len(cells_in_one_row)):
                self.expand_field(field, value)
                if (half[next_row_to_check][cells_in_one_row[i][1]] == 1 - value or
                        (next_row_to_check, cells_in_one_row[i][1]) in possible_to_go_cells or
                        (next_row_to_check, cells_in_one_row[i][1]) in field):
                    go_status = False
                    self.check_field_validity(field)
                    break
            if go_status:
                for i in range(len(cells_in_one_row)):
                    possible_to_go_cells.append((next_row_to_check, cells_in_one_row[i][1]))
                next_row_to_check = 0 if next_row_to_check == len(half) - 1 else next_row_to_check + 1
        return possible_to_go_cells

    def find_equivalence_in_other_half(self, half: list[list[int]], field: list[tuple], value: int) -> list[tuple]:
        other_half_indexes: list[tuple] = []
        self.check_field_validity(field)
        for index in field:
            y = (len(self.map) - 1 - index[1]) % len(half[0])
            if half[index[0]][len(half[0]) - 1 - (index[1] % len(half[0]))] == value:
                other_half_indexes.append((index[0], len(self.map[0]) - 1 - index[1]))
            else:
                return field
        field += other_half_indexes
        return field

    def expand_field(self, field: list[tuple], value: int) -> list[tuple]:
        expanded_field = list(field)
        for (i, j) in field:
            self.calculate_field_perimeter(field)
            if i > 0 and self.map[i - 1][j] == value and (i - 1, j) not in expanded_field:
                expanded_field.append((i - 1, j))
            if i < len(self.map) - 1 and self.map[i + 1][j] == value and (i + 1, j) not in expanded_field:
                expanded_field.append((i + 1, j))
            if j > 0 and self.map[i][j - 1] == value and (i, j - 1) not in expanded_field:
                expanded_field.append((i, j - 1))
            if j < len(self.map[0]) - 1 and self.map[i][j + 1] == value and (i, j + 1) not in expanded_field:
                expanded_field.append((i, j + 1))
        return expanded_field

    def calculate_field_perimeter(self, field: list[tuple]) -> int:
        self.check_field_validity(field)
        perimeter = 0
        for (i, j) in field:
            if (i - 1, j) not in field:
                perimeter += 1
            if (i + 1, j) not in field:
                perimeter += 1
            if (i, j - 1) not in field:
                perimeter += 1
            if (i, j + 1) not in field:
                perimeter += 1
        return perimeter

    def print_table(self):
        line_to_print = '     ' + self.variables[2]
        for i in self.header_line[0]:
            line_to_print += '   ' + i
        print(line_to_print)

        line_to_print = '     ' + self.variables[3]
        for i in self.header_line[1]:
            line_to_print += '   ' + i
        print(line_to_print)

        line_to_print = ' ' + self.variables[0] + ' ' + self.variables[1] + '\\' + self.variables[4]
        for i in self.header_line[2]:
            line_to_print += '   ' + i
        print(line_to_print)

        line_to_print = '-' * len(line_to_print)
        print(line_to_print)

        for i in range(len(self.header_column[0])):
            line_to_print = '  ' + self.header_column[0][i] + ' ' + self.header_column[1][i] + ' '
            for j in range(len(self.header_line[0])):
                line_to_print += ' | ' + str(self.map[i][j])
            print(line_to_print)

    @staticmethod
    def cut_cells_list(index_list: list[tuple], cut_from_end: bool):
        degrees = [1, 2, 4, 8]
        while len(index_list) not in degrees:
            if cut_from_end:
                index_list.pop()
            else:
                index_list.pop(0)
        return index_list


# expression = BooleanExpression('(a~((!b)|(c>(a&(d&f)))))')
#
# karnaugh_method_SDNF = Karnaugh5(expression, 'SDNF')
# karnaugh_method_SDNF.print_table()
# print(karnaugh_method_SDNF.merged_form() + '\n')
#
# karnaugh_method_SKNF = Karnaugh5(expression, 'SKNF')
# karnaugh_method_SKNF.print_table()
# print(karnaugh_method_SKNF.merged_form())
