def replace_character(a: str) -> str:
    """ Replace the characters in the string with the corresponding

    These methods are designed to be an extension of the simplify methods,
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


def analyze_initial_conditions(expr: str):
    expr = expr.replace(' ', '')
    characters = list(expr)

    y0 = ""
    x0 = ""

    count = 0
    while count < len(characters):
        if characters[count] == '(':
            count += 1
            while count < len(characters) and characters[count] != ')':
                y0 += characters[count]
                count += 1
        elif characters[count] == '=':
            count += 1
            x0 = expr[count:]
            break

        count += 1

    return int(y0), int(x0)
