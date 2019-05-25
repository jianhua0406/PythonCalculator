BASE_NUM = '0123456789'
OPERATOR = '+-*/%^'
BRACKETS = '()'
OPERATOR_PRIORITY = {
    '+': 1, '-': 1,
    '*': 2, '/': 2, '%': 2,
    '^':3
}
OPERATOR_NUMBERS = {
    '+': 2,
    '-': 2,
    '*': 2,
    '/': 2,
    '%': 2,
    '^': 2,
}
OPERATOR_CALCULATE = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: x % y,
    '^': lambda x, y: x ** y,
}


def calculate_string(string):
    signals = string_to_signals(string)
    suffixs = infix_to_suffix(signals)
    num = suffix_calculate(suffixs)
    return num


def string_to_signals(string):
    signals = []
    start = -1
    end = 0
    for end in range(len(string)):
        if not is_base_num(string[end]):
            signals.append(string[end])
            start = -1
        else:
            if start == -1:
                start = end
            if end == len(string) - 1 or not is_base_num(string[end + 1]):
                signals.append(int(string[start:end + 1]))
    return signals


def is_base_num(char):
    return char in BASE_NUM


def is_num(signal):
    return isinstance(signal, int)


def is_operator(signal):
    return signal in OPERATOR


def is_brackets(signal):
    return signal in BRACKETS


def operator_compare(signal1, signal2):
    res = OPERATOR_PRIORITY[signal1] - OPERATOR_PRIORITY[signal2]
    if res > 0:
        return 1
    if res < 0:
        return -1
    return 0


def infix_to_suffix(signals):
    stack = []
    suffixs = []
    for signal in signals:
        if is_num(signal):
            suffixs.append(signal)
        elif is_operator(signal):
            while True:
                if len(stack) == 0 or is_brackets(stack[-1]) or operator_compare(signal, stack[-1]) == 1:
                    stack.append(signal)
                    break
                else:
                    suffixs.append(stack.pop())
        elif is_brackets(signal):
            if signal == '(':
                stack.append('(')
            else:
                while True:
                    assert len(stack) > 0
                    if stack[-1] == '(':
                        stack.pop()
                        break
                    suffixs.append(stack.pop())
        else:
            raise Exception('the signal is illegal')
    suffixs += stack[::-1]
    return suffixs


def suffix_calculate(suffixs):
    stack = []
    for suffix in suffixs:
        if is_num(suffix):
            stack.append(suffix)
        elif is_operator(suffix):
            operator_nums = OPERATOR_NUMBERS[suffix]
            if len(stack) < operator_nums:
                raise Exception('input numbers illegal')
            num = OPERATOR_CALCULATE[suffix](*stack[-operator_nums:])
            stack = stack[:-operator_nums]
            stack.append(num)
        else:
            raise Exception('the suffix is illegal')
    assert len(stack) == 1
    return stack[0]
