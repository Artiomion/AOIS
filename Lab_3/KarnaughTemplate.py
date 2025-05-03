from BooleanExpression import BooleanExpression


class KarnaughTemplate:
    def __init__(self, exp: BooleanExpression, form_to_minimize: str):
        self.exp = exp
        self.form_to_minimize = form_to_minimize
        self.variables: list[str] = list(exp.create_variable_dict()[0].keys())
        self.result_values: list[int] = exp.result_values()
        self.index_chain_for_iteration: list[int] = []

    def build_map(self) -> list[list[int]]:
        pass

    def form_final_normal_form_fields(self) -> list[list[tuple]]:
        used_indexes: list[tuple] = []
        fields: list[list[tuple]] = []
        if self.form_to_minimize == 'SDNF':
            value = 1
        else:
            value = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if not (i, j) in used_indexes and self.map[i][j] == value:
                    field = self.form_field(value, (i, j))
                    for index in field:
                        if index not in used_indexes:
                            used_indexes.append(index)
                    self.calculate_field_perimeter(field)
                    fields.append(field)
        return fields

    def form_field(self, value: int, initial_index: tuple) -> list[tuple]:
        ability_to_go: dict = \
            {
                'right': True,
                'left': True,
                'up': True,
                'down': True
            }
        degrees = [1, 2, 4, 8, 16]
        field: list[tuple] = [initial_index]
        equator_is_formed_flag = False
        while ability_to_go['up']:
            last: tuple = field[-1]  # list[-1] -> last el from list
            if ability_to_go['right']:
                if last[1] < len(self.map[0]) - 1:
                    if self.map[last[0]][last[1] + 1] == value and (last[0], last[1] + 1) not in field:
                        field.append((last[0], last[1] + 1))
                    else:
                        ability_to_go['right'] = False
                else:
                    if self.map[last[0]][0] == value and (last[0], 0) not in field:
                        field.append((last[0], 0))
                    else:
                        ability_to_go['right'] = False
            elif ability_to_go['left']:
                if last[1] > 0:
                    if self.map[last[0]][last[1] - 1] == value and (last[0], last[1] - 1) not in field:
                        field.append((last[0], last[1] - 1))
                    else:
                        ability_to_go['left'] = False
                else:
                    # list[-1] -> last el from list
                    if self.map[last[0]][-1] == value and (last[0], len(self.map[0]) - 1) not in field:
                        field.append((last[0], len(self.map[0]) - 1))
                    else:
                        ability_to_go['left'] = False
            else:
                if not equator_is_formed_flag and len(field) not in degrees:
                    field = self.cut_cells_list(field, degrees)
                equator_is_formed_flag = True
                self.calculate_field_perimeter(field)
                if ability_to_go['down']:
                    new_indexes = self.possibility_to_go_down(value, field)
                    field += new_indexes
                    if len(new_indexes) == 0:
                        ability_to_go['down'] = False
                elif ability_to_go['up']:
                    new_indexes = self.possibility_to_go_top(value, field)
                    field += new_indexes
                    if len(new_indexes) == 0:
                        ability_to_go['up'] = False
        if len(field) not in degrees:
            field = self.cut_cells_list(field, degrees)
        return field

    def get_variables_after_merge(self) -> list[list[str]]:
        pass

    def print_table(self):
        pass

    def calculate_field_perimeter(self, field: list[tuple]) -> int:
        pass

    def expand_field(self, field: list[tuple], value: int) -> list[tuple]:
        pass

    def check_field_validity(self, field: list[tuple]) -> bool:
        pass

    def possibility_to_go_top(self, value: int, field: list[tuple]) -> list[tuple]:
        cells_in_one_row: list[tuple] = []
        row_index_from_first_cell: int = field[0][0]
        for i in range(len(field)):
            if field[i][0] != row_index_from_first_cell:
                break
            cells_in_one_row.append(field[i])
        next_row_to_check = len(self.map) - 1 if cells_in_one_row[0][0] == 0 else cells_in_one_row[0][0] - 1
        self.expand_field(field, 1)
        go_status = True
        possible_to_go_cells = []
        while go_status:
            for i in range(len(cells_in_one_row)):
                self.expand_field(field, int(value))
                if ((self.map[next_row_to_check][cells_in_one_row[i][1]] != value) or
                        (next_row_to_check, cells_in_one_row[i][1]) in possible_to_go_cells or
                        ((next_row_to_check, cells_in_one_row[i][1]) in field)):
                    go_status = False
                    self.check_field_validity(field)
                    break
            if go_status:
                for i in range(len(cells_in_one_row)):
                    possible_to_go_cells.append((next_row_to_check, cells_in_one_row[i][1]))
                next_row_to_check = len(self.map) - 1 if next_row_to_check == 0 else next_row_to_check - 1
        return possible_to_go_cells

    def possibility_to_go_down(self, value: int, field: list[tuple]) -> list[tuple]:
        cells_in_one_row: list[tuple] = []
        row_index_from_last_cell: int = field[0][0]
        for i in range(len(field)):
            if field[i][0] != row_index_from_last_cell:
                break
            cells_in_one_row.append(field[i])
        next_row_to_check = 0 if cells_in_one_row[0][0] == len(self.map) - 1 else cells_in_one_row[0][0] + 1
        go_status = True
        self.expand_field(field, 1)
        possible_to_go_cells = []
        while go_status:
            for i in range(len(cells_in_one_row)):
                self.expand_field(field, int(value))
                if (self.map[next_row_to_check][cells_in_one_row[i][1]] != value or
                        (next_row_to_check, cells_in_one_row[i][1]) in possible_to_go_cells or
                        (next_row_to_check, cells_in_one_row[i][1]) in field):
                    go_status = False
                    self.check_field_validity(field)
                    break
            if go_status:
                for i in range(len(cells_in_one_row)):
                    possible_to_go_cells.append((next_row_to_check, cells_in_one_row[i][1]))
                next_row_to_check = 0 if next_row_to_check == len(self.map) - 1 else next_row_to_check + 1
        return possible_to_go_cells

    def merged_form(self) -> str:
        variables: list[list[str]] = self.get_variables_after_merge()  # [[a,b,c],[(!a)],[f,(!d)]]
        if len(variables) == 1 and len(variables[0]) == 0:
            return 'merged form is empty'
        merged_form = ''
        if self.form_to_minimize == 'SDNF':
            separator = '|'
        else:
            separator = '&'
        if self.form_to_minimize == 'SDNF':
            inside_separator = '&'
        else:
            inside_separator = '|'

        for i in range(len(variables)):
            # for list with single variable (no extra brackets)
            if len(variables[i]) == 1 and (len(variables[i][0]) == 4 or len(variables[i][0]) == 1):
                merged_form += variables[i][0]
                if i != len(variables) - 1:
                    merged_form += separator
                continue

            merged_form += '(' + variables[i][0]
            for j in range(1, len(variables[i])):
                merged_form += inside_separator + variables[i][j]
            merged_form += ')'
            if i != len(variables) - 1:
                merged_form += separator
        if len(variables) > 1:
            merged_form = '(' + merged_form + ')'
        return merged_form

    @staticmethod
    def cut_cells_list(index_list: list[tuple], degrees: list[int]):
        while len(index_list) not in degrees:
            index_list.pop()
        return index_list

    def debug_map(self):
        for row in self.map:
            print(' '.join(map(str, row)))
        print()

    def find_not_used_indexes(self):
        not_used_indexes = {index for field in self.form_final_normal_form_fields() for index in field}
        unused_indexes = [(i, j) for i in range(len(self.map)) for j in range(len(self.map[0])) if
                          (i, j) not in not_used_indexes]
        return unused_indexes

    @staticmethod
    def get_positive_binary(decimal_number: int) -> str:
        binary_number = ""
        while decimal_number > 0:
            remainder = decimal_number % 2
            binary_number = str(remainder) + binary_number
            decimal_number = decimal_number // 2
        return binary_number

    @staticmethod
    def to_decimal_form(binary: str) -> int:
        binary.lstrip('0')
        if not len(binary):
            return 0
        decimal: int = 0
        for i in range(len(binary) - 1, -1, -1):
            decimal += int(binary[i]) * pow(2, len(binary) - 1 - i)
        return decimal

