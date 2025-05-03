from BooleanExpression import BooleanExpression


class CalculationMethod:
    def __init__(self, expression: str, form_to_minimize: str):
        self.__form_to_minimize = form_to_minimize
        self.__exp = expression
        self.__sub_expressions = self.__split_expression()
        self.__sub_expressions_variables = self.__split_sub_expressions_variables()
        self.__sub_expressions_values = self.__replace_variables_by_values()
        self.__parent_indexes: dict = {self.__sub_expressions_variables[i].__str__(): [i]
                                       for i in range(len(self.__sub_expressions_variables))}
        self.__sub_expressions_variables_after_merge, self.__sub_expressions_values_after_merge = self.merge()

    def __split_expression(self) -> list[str]:
        sub_expressions = []
        current_sub_exp = ''
        if self.__form_to_minimize == 'SDNF':
            separator = '|'
        else:
            separator = '&'
        for char in self.__exp:
            if char == separator:
                sub_expressions.append(current_sub_exp)
                current_sub_exp = ''
            else:
                current_sub_exp += char

        if current_sub_exp != '':
            sub_expressions.append(current_sub_exp)
        return sub_expressions

    def __split_sub_expressions_variables(self) -> list[list[str]]:
        variables = []
        for i in range(len(self.__sub_expressions)):
            variables.append([])
            current_sub_exp = self.__sub_expressions[i]
            for j in range(len(current_sub_exp)):
                if 'a' <= current_sub_exp[j] <= 'z':
                    variables[i].append(
                        ('(!' + current_sub_exp[j] + ')') if current_sub_exp[j - 1] == '!' else current_sub_exp[j])
        return variables

    def __replace_variables_by_values(self) -> list[list[int]]:
        sub_expressions_values = []
        for i in range(len(self.__sub_expressions_variables)):
            sub_expressions_values.append([])
            for variable in self.__sub_expressions_variables[i]:
                if len(variable) == 1:
                    sub_expressions_values[i].append(1)
                else:
                    sub_expressions_values[i].append(0)
        return sub_expressions_values

    def merge(self) -> (list[list[str]], list[list[bool]]):
        variables = self.__sub_expressions_variables
        values = self.__sub_expressions_values
        loop_exit = False
        while not loop_exit:
            variables, values, loop_exit = self.uniting(variables, values)
        new_values = values.copy()
        new_variables = variables.copy()
        self.__get_variable_frequency()
        for i in range(len(new_values)):
            # mark by -1 value of variable to unite
            minuses_amount = 0
            for value in new_values[i]:
                if value == -1:
                    minuses_amount += 1
            if len(new_values[i]) - minuses_amount != len(new_variables[i]):
                variables.remove(new_variables[i])
                values.remove(new_values[i])
        return variables, values

    def uniting(self, expressions_variables: list[list[str]], expressions_values: list[list[int]]):
        united_expression_variables = []
        united_expression_values = []
        loop_exit = False
        marked_as_used = [False] * len(expressions_variables)
        for i in range(len(expressions_variables) - 1):
            for j in range(i + 1, len(expressions_variables)):
                ready_status, dif_val_pos, dif_var_pos = self.check_ready_for_unite(len(expressions_variables[i]) - 1,
                                                                                    expressions_values[i],
                                                                                    expressions_values[j],)
                if ready_status:
                    i_parent_indexes = self.__parent_indexes[expressions_variables[i].__str__()][:]
                    j_parent_indexes = self.__parent_indexes[expressions_variables[j].__str__()]
                    for index in j_parent_indexes:
                        if index not in i_parent_indexes:
                            i_parent_indexes.append(index)

                    marked_as_used[i] = True
                    marked_as_used[j] = True
                    temp_uniting_variables, temp_uniting_values = self.uniting_lists(expressions_variables[i],
                                                                                     expressions_values[i],
                                                                                     dif_var_pos,
                                                                                     dif_val_pos)
                    united_expression_variables.append(temp_uniting_variables)
                    united_expression_values.append(temp_uniting_values)
                    self.__extract_unique_variables()
                    self.__parent_indexes[temp_uniting_variables.__str__()] = i_parent_indexes
        not_marked_as_used = 0
        for i in range(len(marked_as_used)):
            if not marked_as_used[i]:
                not_marked_as_used += 1
                united_expression_variables.append(expressions_variables[i])
                united_expression_values.append(expressions_values[i])
        if not_marked_as_used == len(marked_as_used):
            loop_exit = True
        return united_expression_variables, united_expression_values, loop_exit

    @staticmethod
    def check_ready_for_unite(asked_amount_of_variables: int, first_exp_values: list[int], sec_exp_values: list[int]):
        if CalculationMethod.indexes_with_minus_value(first_exp_values) != \
                CalculationMethod.indexes_with_minus_value(sec_exp_values):
            return False, 0, 0
        dif_value_pos = 0
        present_count_of_variables = 0
        for i in range(len(first_exp_values)):
            if first_exp_values[i] != -1 and sec_exp_values[i] != -1:
                if first_exp_values[i] == sec_exp_values[i]:
                    present_count_of_variables += 1
                else:
                    dif_value_pos = i
        if present_count_of_variables != asked_amount_of_variables:
            return False, 0, 0
        minuses_before_dif_pos = 0
        for i in range(dif_value_pos):
            if first_exp_values[i] == -1:
                minuses_before_dif_pos += 1
        dif_variable_pos = dif_value_pos - minuses_before_dif_pos
        return True, dif_value_pos, dif_variable_pos

    @staticmethod
    def indexes_with_minus_value(values: list[int]) -> list[int]:
        # mark by -1 value of variable to unite
        indexes = []
        for i in range(len(values)):
            if values[i] == -1:
                indexes.append(i)
        return indexes

    @staticmethod
    def uniting_lists(expressions_variables: list[str], expression_values: list[int], dif_var_pos: int,
                      dif_value_pos: int) -> (list[str], list[bool]):
        uniting_variables = []
        uniting_values = expression_values[:]
        for i in range(len(expressions_variables)):
            if i != dif_var_pos:
                uniting_variables.append(expressions_variables[i])
            elif i == dif_value_pos:
                # mark by -1 value of variable to unite
                uniting_values[i] = -1
        return uniting_variables, uniting_values

    def merged_form(self):
        result = ''
        result_sub_exps: list[list[str]] = []
        if self.__form_to_minimize == 'SDNF':
            separator = '|'
        else:
            separator = '&'

        if self.__form_to_minimize == 'SDNF':
            inside_separator = '&'
        else:
            inside_separator = '|'

        for sub_epx in self.__sub_expressions_variables_after_merge:
            result_sub_exps.append(sub_epx)
        for i in range(len(result_sub_exps) - 1):
            inside_exp = ''
            for j in range(len(result_sub_exps[i]) - 1):
                inside_exp += '(' + result_sub_exps[i][j] + inside_separator
            inside_exp += result_sub_exps[i][-1] + ')' * (len(result_sub_exps[i]) - 1)  # list[-1] -> last el from list
            result += '(' + inside_exp + separator

        inside_exp = ''
        last_sub_exp = result_sub_exps[len(result_sub_exps) - 1]
        for i in range(len(last_sub_exp) - 1):
            inside_exp += '(' + last_sub_exp[i] + inside_separator
        inside_exp += last_sub_exp[-1] + ')' * (len(last_sub_exp) - 1)

        if len(result) == 0:
            final_form_is_empty = True
        else:
            final_form_is_empty = False

        if final_form_is_empty:
            result += '('
        result += inside_exp
        result += ')' * (len(result_sub_exps) - 1)
        if final_form_is_empty:
            result += ')'
        if len(result_sub_exps) == 1:
            result = result[1:len(result) - 1]
        return result

    def __get_variable_frequency(self) -> dict:
        variable_frequency = {}
        for variable_list in self.__sub_expressions_variables:
            for variable in variable_list:
                variable_frequency[variable] = variable_frequency.get(variable, 0) + 1
        return variable_frequency

    def __extract_unique_variables(self) -> set:
        unique_variables = set()
        for variable_list in self.__sub_expressions_variables:
            for variable in variable_list:
                unique_variables.add(variable)
        return unique_variables

    def __validate_expression_syntax(self):
        if not isinstance(self.__exp, str):
            raise TypeError("Выражение должно быть строкой")
        if not self.__exp:
            raise ValueError("Выражение не может быть пустым")
        allowed_chars = set('abcdefghijklmnopqrstuvwxyz!|&()~>')
        if not all(char in allowed_chars for char in self.__exp):
            raise ValueError("Выражение содержит недопустимые символы")

    @property
    def form_to_minimize(self):
        return self.__form_to_minimize

    @property
    def sub_expressions(self):
        return self.__sub_expressions

    @property
    def parent_indexes(self):
        return self.__parent_indexes

    @property
    def sub_expressions_variables(self):
        return self.__sub_expressions_variables

    @property
    def sub_expressions_values(self):
        return self.__sub_expressions_values

    @property
    def sub_expressions_variables_after_merge(self):
        return self.__sub_expressions_variables_after_merge


# expression = BooleanExpression('((!a)|(d~c))')
#
# SDNF = expression.build_SDNF()
# print('SDNF\n' + SDNF)
#
# calculation_method = CalculationMethod(SDNF, 'SDNF')
# merged_by_SDNF = calculation_method.merged_form()
# print('merged by SDNF expression\n' + merged_by_SDNF)
#
# SKNF = expression.build_SKNF()
# print('SKNF\n' + SKNF)
#
# calculation_method = CalculationMethod(SKNF, 'SKNF')
# merged_by_SKNF = calculation_method.merged_form()
# print('merged by SKNF expression\n' + merged_by_SKNF)
