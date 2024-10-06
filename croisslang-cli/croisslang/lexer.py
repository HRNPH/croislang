import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.tokens = []

    def tokenize(self):
        patterns = {
            "MEMORY_SIZE": r"Oven<\d+>",   # Matches Oven<8>
            "BINARY": r"[01]",             # Matches 0 or 1 (binary digits)
            "NUMBER": r"\d+",              # Matches numbers for positions, etc.
            "IDENTIFIER": r"[A-Za-z_][A-Za-z0-9_]*",
            "LBRACE": r"<",                # Matches the opening <
            "RBRACE": r">",                # Matches the closing >
            "COMMA": r",",                 # Matches commas between binary digits
            "BAKE": r"Bake",
            "FLIP": r"Flip",
            "SHIFT": r"Shift",
            "PREPARE": r"Prepare",
            "COMBINE": r"Combine",
            "SERVE": r"Serve",
            "IF": r"If",
            "ELSE": r"Otherwise",
            "COOKED": r"cooked",
            "LEFT": r"left",
            "INTO": r"into",
            "WITH": r"with",
            "AT": r"at",
            "TIMES": r"times",
        }

        while self.position < len(self.text):
            if self.text[self.position].isspace():
                self.position += 1
                continue

            for token_type, pattern in patterns.items():
                regex = re.compile(pattern)
                match = regex.match(self.text, self.position)
                if match:
                    value = match.group(0)
                    self.tokens.append(Token(token_type, value))
                    self.position += len(value)
                    break
            else:
                current_char = self.text[self.position]
                raise ValueError(f"Unexpected character '{current_char}' at position {self.position}")

        return self.tokens