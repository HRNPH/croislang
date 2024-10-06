from croisslang.lexer import Token, Lexer

class ASTNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        nodes = []
        while self.position < len(self.tokens):
            node = self.parse_statement()
            if node:
                nodes.append(node)
        return nodes

    def parse_statement(self):
        token = self.current_token()
        
        if token.type == "MEMORY_SIZE":
            return self.parse_oven()
        elif token.type == "PREPARE":
            return self.parse_prepare()
        elif token.type == "FLIP":
            return self.parse_flip()
        elif token.type == "SHIFT":
            return self.parse_shift()
        elif token.type == "COMBINE":
            return self.parse_combine()
        elif token.type == "BAKE":
            return self.parse_bake_loop()
        elif token.type == "IF":
            return self.parse_if_else()
        elif token.type == "SERVE":
            return self.parse_serve()
        elif token.type == "OUT":
            return ASTNode("BakeComplete")

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
        return ASTNode("Oven", int(size))

    def parse_prepare(self):
        self.consume_token("PREPARE")
        croissant = self.consume_token("LBRACE").value
        self.consume_token("RBRACE")
        self.consume_token("INTO")
        tray_name = self.consume_token("IDENTIFIER").value
        return ASTNode("Prepare", {"croissant": croissant, "tray": tray_name})

    def parse_flip(self):
        self.consume_token("FLIP")
        tray = self.consume_token("IDENTIFIER").value
        self.consume_token("AT")
        position = self.consume_token("NUMBER").value
        return ASTNode("Flip", {"tray": tray, "position": int(position)})

    def parse_shift(self):
        self.consume_token("SHIFT")
        tray = self.consume_token("IDENTIFIER").value
        direction = self.consume_token("LEFT").value  # Only left for now
        self.consume_token("BY")
        steps = self.consume_token("NUMBER").value
        return ASTNode("Shift", {"tray": tray, "direction": direction, "steps": int(steps)})

    def parse_combine(self):
        self.consume_token("COMBINE")
        tray1 = self.consume_token("IDENTIFIER").value
        self.consume_token("WITH")
        tray2 = self.consume_token("IDENTIFIER").value
        self.consume_token("INTO")
        result_tray = self.consume_token("IDENTIFIER").value
        return ASTNode("Combine", {"tray1": tray1, "tray2": tray2, "result": result_tray})

    def parse_bake_loop(self):
        self.consume_token("BAKE")
        times = self.consume_token("NUMBER").value
        bake_node = ASTNode("BakeLoop", int(times))
        while self.current_token().type != "SERVE" and self.current_token().type != "OUT":
            statement = self.parse_statement()
            if statement:
                bake_node.add_child(statement)
        return bake_node

    def parse_if_else(self):
        self.consume_token("IF")
        tray = self.consume_token("IDENTIFIER").value
        self.consume_token("COOKED")
        if_node = ASTNode("IfCooked", tray)
        while self.current_token().type != "SERVE" and self.current_token().type != "OUT":
            statement = self.parse_statement()
            if statement:
                if_node.add_child(statement)
        if self.current_token().type == "ELSE":
            self.consume_token("ELSE")
            else_node = ASTNode("Else")
            while self.current_token().type != "SERVE" and self.current_token().type != "OUT":
                statement = self.parse_statement()
                if statement:
                    else_node.add_child(statement)
            if_node.add_child(else_node)
        return if_node

    def parse_serve(self):
        self.consume_token("SERVE")
        tray = self.consume_token("IDENTIFIER").value
        return ASTNode("Serve", tray)
