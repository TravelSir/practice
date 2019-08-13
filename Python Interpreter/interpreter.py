# -*- coding: utf-8 -*-
class Interpreter(object):

    def __init__(self):
        self.stack = []
        # 存储变量映射关系的字典变量
        self.environment = {}

    def store_name(self, name):
        val = self.stack.pop()
        self.environment[name] = val

    def load_name(self, name):
        val = self.environment[name]
        self.stack.append(val)

    def load_value(self, number):
        self.stack.append(number)

    def print_answer(self):
        answer = self.stack.pop()
        print(answer)

    def add_two_values(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

    def parse_argument(self, instruction, argument, what_to_execute):
        # 解析命令参数
        # 使用常量列表的方法
        numbers = ["load_value"]
        # 使用变量名列表的方法
        names = ["load_name", "store_name"]

        if instruction in numbers:
            argument = what_to_execute["numbers"][argument]
        elif instruction in names:
            argument = what_to_execute["names"][argument]

        return argument

    def run_code(self, what_to_execute):
        # 指令列表
        instructions = what_to_execute["instructions"]
        # 常数列表
        numbers = what_to_execute["numbers"]
        # 遍历指令列表，一个一个执行
        for each_step in instructions:
            # 得到指令和对应参数
            instruction, argument = each_step
            if instruction == "load_value":
                number = numbers[argument]
                self.load_value(number)
            elif instruction == "add_two_values":
                self.add_two_values()
            elif instruction == "print_answer":
                self.print_answer()

    def execute(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, what_to_execute)
            bytecode_method = getattr(self, instruction)
            if argument is None:
                bytecode_method()
            else:
                bytecode_method(argument)


if __name__ == '__main__':
    what_to_execute = {
        "instructions": [("load_value", 0),  # 第一个数
                         ("load_value", 1),  # 第二个数
                         ("add_two_values", None),
                         ("print_answer", None)],
        "numbers": [7, 5]
    }
    interpreter = Interpreter()
    interpreter.run_code(what_to_execute)

