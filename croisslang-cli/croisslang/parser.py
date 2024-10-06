from tqdm import tqdm
import re

class ASTNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)
# Refactoring the parser logic to correctly handle binary digits and the closing brace

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.memory_limit = 0
        self.memory_used = 0

    def parse(self):
        nodes = []
        total_statements = len(self.tokens)

        while self.position < len(self.tokens):
            node = self.parse_statement()
            if node:
                nodes.append(node)
            else:
                break  # Break out of the loop if no valid node is found

        return nodes

    def parse_statement(self):
        token = self.current_token()

        if token is None:
            return None

        if token.type == "MEMORY_SIZE":
            return self.parse_oven()
        elif token.type == "IDENTIFIER" and token.value == "Prepare":
            return self.parse_prepare()
        elif token.type == "IDENTIFIER" and token.value == "Flip":
            return self.parse_flip()
        elif token.type == "IDENTIFIER" and token.value == "Combine":
            return self.parse_combine()
        elif token.type == "IDENTIFIER" and token.value == "Serve":
            return self.parse_serve()
        elif token.type == "IDENTIFIER" and token.value == "Bake":
            return self.parse_bake_loop()

    def parse_bake_loop(self):
        self.consume_token("IDENTIFIER")  # Consume "Bake"
        times = int(self.consume_token("NUMBER").value)  # The number of iterations
        bake_node = ASTNode("BakeLoop", times)

        # Parse all inner statements inside the loop until the loop ends or Serve is reached
        while self.current_token() and self.current_token().type == "IDENTIFIER" and self.current_token().value != "Serve":
            statement = self.parse_statement()
            if statement:
                bake_node.add_child(statement)
        
        return bake_node

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def consume_token(self, token_type=None):
        token = self.current_token()
        if token_type and token.type != token_type:
            raise ValueError(f"Expected token {token_type} but got {token.type}")
        self.position += 1
        return token

    def parse_oven(self):
        token = self.consume_token("MEMORY_SIZE")
        size = re.findall(r"\d+", token.value)[0]
        self.memory_limit = int(size)
        return ASTNode("Oven", int(size))

    def parse_prepare(self):
        self.consume_token("IDENTIFIER")  # Consume "Prepare"
        self.consume_token("LBRACE")  # Matches <
        croissant = []
        while self.current_token().type in ["BINARY", "COMMA"]:
            if self.current_token().type == "BINARY":
                croissant.append(self.consume_token("BINARY").value)
            elif self.current_token().type == "COMMA":
                self.consume_token("COMMA")  # Skip the comma
        self.consume_token("RBRACE")  # Matches >
        self.consume_token("IDENTIFIER")  # Matches "into"
        tray_name = self.consume_token("IDENTIFIER").value

        # Calculate memory usage for the croissant and enforce memory limit
        croissant_size = len(croissant)
        self.memory_used += croissant_size
        if self.memory_used > self.memory_limit:
            raise ValueError(f"Memory overflow. Tried to store {self.memory_used} bits in an oven with a capacity of {self.memory_limit} bits.")

        return ASTNode("Prepare", {"croissant": ''.join(croissant), "tray": tray_name})

    def parse_flip(self):
        self.consume_token("IDENTIFIER")  # Consume "Flip"
        tray = self.consume_token("IDENTIFIER").value
        self.consume_token("IDENTIFIER")  # Matches "at"
        position = self.consume_token("NUMBER").value
        return ASTNode("Flip", {"tray": tray, "position": int(position)})

    def parse_combine(self):
        self.consume_token("IDENTIFIER")  # Consume "Combine"
        tray1 = self.consume_token("IDENTIFIER").value
        self.consume_token("IDENTIFIER")  # Matches "with"
        tray2 = self.consume_token("IDENTIFIER").value
        self.consume_token("IDENTIFIER")  # Matches "into"
        result_tray = self.consume_token("IDENTIFIER").value
        return ASTNode("Combine", {"tray1": tray1, "tray2": tray2, "result": result_tray})

    def parse_serve(self):
        self.consume_token("IDENTIFIER")  # Consume "Serve"
        tray = self.consume_token("IDENTIFIER").value
        return ASTNode("Serve", tray)