def karnaugh_simplification(expression):
    def count_ones(n):
        count = 0
        while n:
            count += n & 1
            n >>= 1
        return count

    def combine_terms(terms, num_vars):
        combined_terms = []
        for term1 in terms:
            for term2 in terms:
                diff = term1 ^ term2
                if count_ones(diff) == 1:
                    mask = 1 << (num_vars - 1)
                    combined_term = term1 & term2
                    combined_mask = 0
                    for _ in range(num_vars):
                        combined_mask <<= 1
                        if diff & mask:
                            combined_mask |= 1
                        mask >>= 1
                    combined_terms.append((combined_term, combined_mask))
        return combined_terms

    def simplify_terms(terms, num_vars):
        simplified_terms = []
        while terms:
            term, mask = terms.pop(0)
            covered_terms = [term]
            for i, (other_term, other_mask) in enumerate(terms[:]):
                if (term & mask) == (other_term & mask):
                    covered_terms.append(other_term)
                    terms.pop(i)
            if len(covered_terms) == 1:
                simplified_terms.append((term, mask))
        return simplified_terms

    def term_to_expression(term, num_vars):
        expression = ''
        for i in range(num_vars):
            if term & (1 << (num_vars - 1 - i)):
                expression += chr(ord('A') + i)
            else:
                expression += chr(ord('A') + i) + '\''
        return expression

    def binary_to_gray(n):
        return n ^ (n >> 1)

    def expression_to_kmap(expression):
        num_vars = max([ord(c) - ord('A') + 1 for c in expression])
        kmap = [['0' for _ in range(2 ** (num_vars - 1))] for _ in range(2 ** (num_vars - 1))]
        for i in range(2 ** num_vars):
            binary = "{:0{}b}".format(i, num_vars)
            gray = binary_to_gray(i)
            row = gray >> (num_vars - 1)
            col = gray % (2 ** (num_vars - 1))
            kmap[row][col] = '1' if expression_to_truth(expression, binary) else '0'
        return kmap

    def expression_to_truth(expression, binary):
        values = {}
        for i, var in enumerate(sorted(set(expression))):
            values[var] = bool(int(binary[i].zfill))
            values[var.lower()] = not values[var]
        return eval(expression, values)

    def simplify_expression(expression):
        num_vars = max([ord(c) - ord('A') + 1 for c in expression])
        terms = []
        for i in range(2 ** num_vars):
            if expression_to_truth(expression, format(i, '0{}b'.format(num_vars))):
                terms.append(i)
        combined_terms = [(term, 2 ** num_vars - 1) for term in terms]
        while True:
            new_combined_terms = combine_terms([term for term, _ in combined_terms], num_vars)
            new_simplified_terms = simplify_terms(new_combined_terms, num_vars)
            if new_combined_terms == combined_terms:
                break
            combined_terms = new_simplified_terms
        simplified_expression = ' + '.join([term_to_expression(term, num_vars) for term, _ in combined_terms])
        return simplified_expression

    simplified_expression = simplify_expression(expression)
    return simplified_expression


expression =input("Entrer la fonction logique")
simplified_expression = karnaugh_simplification(expression)
print("Simplified expression:", simplified_expression)