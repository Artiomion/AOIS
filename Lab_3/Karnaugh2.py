from KarnaughTemplate import KarnaughTemplate, BooleanExpression


class Karnaugh2(KarnaughTemplate):
    def __init__(self, exp: BooleanExpression, form_to_minimize: str):
        self.header_line = ['0', '1']
        self.header_column = ['0', '1']
        super().__init__(exp, form_to_minimize)
        self.map: list[list[int]] = self.build_map()

    def build_map(self) -> list[list[int]]:
        for i in self.header_column:
            for j in self.header_line:
                self.index_chain_for_iteration.append(self.to_decimal_form(i + j))
        table = []
        counter = 0
        for i in range(len(self.header_column)):
            table.append([])
            for j in range(len(self.header_line)):
                table[i].append(self.result_values[self.index_chain_for_iteration[counter]])
                counter += 1
        return table

    def check_field_validity(self, field: list[tuple]) -> bool:
        # check if all cells has same value
        if not field:
            return False
        first_value = self.map[field[0][0]][field[0][1]]
        return all(self.map[i][j] == first_value for i, j in field)

    def get_variables_after_merge(self) -> list[list[str]]:
        fields: list[list[tuple]] = self.form_final_normal_form_fields()
        if self.form_to_minimize == 'SDNF':
            value = '1'
        else:
            value = '0'
        variables: list[list[str]] = []
        for i in range(len(fields)):
            initial_values: list[str] = [self.header_column[fields[i][0][0]], self.header_line[fields[i][0][1]]]
            different: list[bool] = [False] * len(self.variables)
            self.expand_field(fields[i], int(value))
            for cell in fields[i]:
                if self.header_line[cell[1]] != initial_values[1]:
                    different[1] = True
                elif self.header_column[cell[0]] != initial_values[0]:
                    different[0] = True
            final_variables_from_field: list[str] = []
            for j in range(len(different)):
                if not different[j]:
                    final_variables_from_field.append(self.variables[j] if initial_values[j] == value
                                                      else '(!' + self.variables[j] + ')')
            variables.append(final_variables_from_field)
        return variables

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

    def expand_field(self, field: list[tuple], value: int) -> list[tuple]:
        expanded_field = list(field)
        self.check_field_validity(expanded_field)
        for (i, j) in field:
            if i > 0 and self.map[i - 1][j] == value and (i - 1, j) not in expanded_field:
                expanded_field.append((i - 1, j))
            if i < len(self.map) - 1 and self.map[i + 1][j] == value and (i + 1, j) not in expanded_field:
                expanded_field.append((i + 1, j))
            if j > 0 and self.map[i][j - 1] == value and (i, j - 1) not in expanded_field:
                expanded_field.append((i, j - 1))
            if j < len(self.map[0]) - 1 and self.map[i][j + 1] == value and (i, j + 1) not in expanded_field:
                expanded_field.append((i, j + 1))
        return expanded_field

    def print_table(self):
        line_to_print = ' ' + self.variables[0] + '\\' + self.variables[1]
        for i in self.header_line:
            line_to_print += '   ' + i
        print(line_to_print)

        line_to_print = '-' * len(line_to_print)
        print(line_to_print)

        for i in range(len(self.header_line)):
            line_to_print = '  ' + self.header_column[i] + ' '
            for j in range(len(self.header_line)):
                line_to_print += ' | ' + str(self.map[i][j])
            print(line_to_print)


# expression = BooleanExpression('(a~((!a)|b))')
#
# karnaugh_method_SDNF = Karnaugh2(expression, 'SDNF')
# karnaugh_method_SDNF.print_table()
# print(karnaugh_method_SDNF.merged_form() + '\n')
#
# karnaugh_method_SKNF = Karnaugh2(expression, 'SKNF')
# karnaugh_method_SKNF.print_table()
# print(karnaugh_method_SDNF.merged_form())

