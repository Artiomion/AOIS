from pythonds.basic.stack import Stack
from pythonds.trees.binaryTree import BinaryTree


class BooleanExpression:

    def __init__(self, exp):
        self.__exp = exp
        self.__index_by_variable_dict, self.__variable_by_index_dict = self.__create_variable_dict()
        self.__syntax_tree = self.create_syntax_tree(exp)

    def __create_variable_dict(self):
        list_of_variables = []
        for i in self.__exp:
            if 'a' <= i <= 'z' and i not in list_of_variables:
                list_of_variables.append(i)
        list_of_variables.sort()
        index_by_variable_dict = {}
        variable_by_index_dict = {}
        for i in range(0, len(list_of_variables)):
            index_by_variable_dict[list_of_variables[i]] = i
            variable_by_index_dict[i] = list_of_variables[i]
        return index_by_variable_dict, variable_by_index_dict

    @staticmethod
    def create_syntax_tree(exp):
        stack_of_parents = Stack()
        syntax_tree = BinaryTree([])
        present_tree = syntax_tree
        stack_of_parents.push(syntax_tree)
        for i in range(len(exp)):
            if exp[i] == '(':
                present_tree.insertLeft([])
                present_tree.setRootVal([i])
                stack_of_parents.push(present_tree)
                present_tree = present_tree.getLeftChild()
            elif exp[i] not in ['(', ')', '!', '&', '|', '~', '>']:
                present_tree.setRootVal([exp[i]])
                parent = stack_of_parents.pop()
                present_tree = parent
            elif exp[i] == ')':
                present_tree_root_list = present_tree.getRootVal()
                present_tree_root_list.append(i)
                present_tree.setRootVal(present_tree_root_list)
                present_tree = stack_of_parents.pop()
            elif exp[i] == '!':
                parent = stack_of_parents.pop()
                parent_root_list = parent.getRootVal()
                parent_root_list.insert(0, '!')
                parent.setRootVal(parent_root_list)
                stack_of_parents.push(parent)
            elif exp[i] in ['&', '|', '>', '~']:
                present_tree_root_list = present_tree.getRootVal()
                present_tree_root_list.insert(0, exp[i])
                present_tree.setRootVal(present_tree_root_list)
                present_tree.insertRight([])
                stack_of_parents.push(present_tree)
                present_tree = present_tree.getRightChild()
            else:
                raise ValueError
        return syntax_tree

    def calculate(self, syntax_tree, variable_values, exp):
        left_child, right_child = syntax_tree.getLeftChild(), syntax_tree.getRightChild()
        operations = {'&': self.con,
                      '|': self.dis,
                      '!': self.neg,
                      '>': self.impl,
                      '~': self.equ}
        if not left_child and not right_child:
            return variable_values[self.__index_by_variable_dict[syntax_tree.getRootVal()[0]]]
        elif left_child and not right_child:
            return self.neg(self.calculate(left_child, variable_values, exp))
        if left_child and right_child:
            operation = operations[syntax_tree.getRootVal()[0]]
            return operation(self.calculate(left_child, variable_values, exp),
                             self.calculate(right_child, variable_values, exp))

    def truth_table(self):
        truth_table, list_of_subtrees = [], []
        add_all_subtrees_to_trees_list(self.__syntax_tree, list_of_subtrees, self.exp)
        list_of_subtrees.reverse()
        amount_of_variables = len(self.__variable_by_index_dict)

        header = ''
        for i in range(0, len(self.__variable_by_index_dict)):
            header += self.__variable_by_index_dict[i] + ' '
        for i in list_of_subtrees:
            header += i.exp + ' '
        truth_table.append(header)

        interpretation = [False for i in range(amount_of_variables)]
        for i in range(0, 2 ** amount_of_variables):
            print_line = ''
            for j in interpretation:
                print_line += str(int(j)) + ' '
            for j in list_of_subtrees:
                space_buffer = ' ' * (len(j.exp) // 2)
                print_line += space_buffer \
                              + str(int(self.calculate(j.syntax_tree, interpretation, j.exp))) \
                              + space_buffer
            truth_table.append(print_line)
            self.next_interpretation(interpretation)
        return truth_table

    @staticmethod
    def next_interpretation(interpretation):
        i = len(interpretation) - 1
        while interpretation[i]:
            interpretation[i] = False
            i -= 1
        interpretation[i] = True
        return interpretation

    def result_values(self):
        amount_of_variables = len(self.__variable_by_index_dict)
        interpretation = [False for i in range(amount_of_variables)]
        result = []
        for i in range(0, 2 ** amount_of_variables):
            result.append(int(self.calculate(self.syntax_tree, interpretation, self.exp)))
            self.next_interpretation(interpretation)
        return result

    def build_SDNF(self):
        amount_of_variables = len(self.__variable_by_index_dict)
        SDNF = ''
        result_values = self.result_values()
        for i in range(len(result_values)):
            if result_values[i] == 1:
                if SDNF != '':
                    SDNF += '|'
                SDNF += '('
                values = to_binary_form(i)
                for j in range(0, amount_of_variables - len(values)):
                    values.insert(0, False)
                for j in range(0, amount_of_variables):
                    if not values[j]:
                        SDNF += '(!' + self.__variable_by_index_dict[j] + ')&'
                    else:
                        SDNF += self.__variable_by_index_dict[j] + '&'
                SDNF = SDNF[:len(SDNF) - 1]
                SDNF += ')'
        return SDNF

    def build_SKNF(self):
        amount_of_variables = len(self.__variable_by_index_dict)
        SKNF = ''
        result_values = self.result_values()
        for i in range(len(result_values)):
            if result_values[i] == 0:
                if SKNF != '':
                    SKNF += '&'
                SKNF += '('
                values = to_binary_form(i)
                for j in range(0, amount_of_variables - len(values)):
                    values.insert(0, False)
                for j in range(0, amount_of_variables):
                    if values[j]:
                        SKNF += '(!' + self.__variable_by_index_dict[j] + ')|'
                    else:
                        SKNF += self.__variable_by_index_dict[j] + '|'
                SKNF = SKNF[:len(SKNF) - 1]
                SKNF += ')'
        return SKNF

    def build_numeric_forms(self):
        result_values = self.result_values()
        SDNF, SKNF = [], []
        for i in range(len(result_values)):
            if result_values[i] == 1:
                SDNF.append(i)
            else:
                SKNF.append(i)
        SDNF_numeric, SKNF_numeric = '(', '('
        for i in range(0, len(SDNF)):
            SDNF_numeric += str(SDNF[i]) + ' '
        for i in range(0, len(SKNF)):
            SKNF_numeric += str(SKNF[i]) + ' '
        SDNF_numeric += ') |'
        SKNF_numeric += ') &'
        return SDNF_numeric, SKNF_numeric

    def build_index_form(self):
        result_values = self.result_values()
        index_form = to_decimal_form(result_values)
        line_to_print = str(index_form) + ' - '
        for i in result_values:
            line_to_print += str(i)
        return line_to_print

    @property
    def exp(self):
        return self.__exp

    @exp.setter
    def exp(self, new_exp):
        self.__exp = new_exp

    @property
    def syntax_tree(self):
        return self.__syntax_tree

    @syntax_tree.setter
    def syntax_tree(self, new_syntax_tree):
        self.__syntax_tree = new_syntax_tree

    @staticmethod
    def con(exp1, exp2):
        return exp1 and exp2

    @staticmethod
    def dis(exp1, exp2):
        return exp1 or exp2

    @staticmethod
    def neg(exp):
        return not exp

    @staticmethod
    def impl(exp1, exp2):
        return (not exp1) or exp2

    @staticmethod
    def equ(exp1, exp2):
        return exp1 == exp2


def add_all_subtrees_to_trees_list(present_tree, trees_list, exp):
    if len(present_tree.getRootVal()) > 1:
        # expression from '(' index to ')' index + 1
        trees_list.append(BooleanExpression(
            exp[present_tree.getRootVal()[1]:present_tree.getRootVal()[2] + 1]))
    if present_tree.getLeftChild():
        add_all_subtrees_to_trees_list(present_tree.getLeftChild(), trees_list, exp)
    if present_tree.getRightChild():
        add_all_subtrees_to_trees_list(present_tree.getRightChild(), trees_list, exp)


def to_binary_form(number):
    binary_number = []
    while number > 0:
        binary_number.insert(0, bool(number % 2))
        number //= 2
    return binary_number


def to_decimal_form(binary_list):
    number = 0
    for i in range(len(binary_list)):
        number += binary_list[i] * (2 ** (len(binary_list) - 1 - i))
    return number


exp = BooleanExpression('((!(a&(!b)))>c)')
for i in exp.truth_table():
    print(i)
print('СДНФ\n' + exp.build_SDNF())
print('СКНФ\n' + exp.build_SKNF())
print('Числовая форма')
SDNF_num, SKNF_num = exp.build_numeric_forms()
print(SDNF_num + '\n' + SKNF_num)
print('Индексная форма\n' + exp.build_index_form())
