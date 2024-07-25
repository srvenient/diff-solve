from sympy import Eq, sympify, latex


def _replace_chars(a: str) -> str:
    """ Replace the characters in the string with the corresponding

    This method is designed to be an extension of the sympify method,
    since it does not recognize some expressions, such as y'.

    :param a: The string to be replaced
    :return: The string with the characters replaced
    """
    eq = list(a)
    result = []
    count = 0

    while count < len(eq):
        c = eq[count]

        if c == 'y':
            # Check if the next character is a prime symbol
            if count + 1 < len(eq) and eq[count + 1] == "'":
                d, p = count + 1, 0
                while d < len(eq) and eq[d] == "'":
                    p += 1
                    d += 1  # Count the number of prime symbols

                if d < len(eq) and eq[d] == '(':
                    i = d + 1
                    text = ""
                    while i < len(eq) and eq[i] != ')':
                        text += eq[i]
                        i += 1

                    result.append("Derivative(y, {}, {})".format(text, p))
                    count = i + 1  # Move count past the closing parenthesis
                else:
                    result.append("Derivative(y, x, {})".format(p))
                    count = d  # Move count past the prime symbols
                continue

            if count + 1 < len(eq) and eq[count + 1] == '(':
                i = count + 2
                text = ""
                while i < len(eq) and eq[i] != ')':
                    text += eq[i]
                    i += 1
                result.append("Function(y)({})".format(text))
                count = i + 1  # Move count past the closing parenthesis
                continue

            # If the character is not a prime symbol, add the variable to the token
            result.append('y')
        else:
            result.append(c)

        count += 1

    return ''.join(result)


def get_as_equation(a: str) -> Eq:
    """ Convert the string to a sympy equation

    :param a: The string to be converted
    :return: The sympy equation
    """
    l, s = a.strip().split("=")
    try:
        left = sympify(_replace_chars(l))
        right = sympify(_replace_chars(s))

        return Eq(left, right)
    except Exception as e:
        raise ValueError("Invalid expression") from e
