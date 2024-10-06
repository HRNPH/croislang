from croisslang.parser import Parser
from croisslang.lexer import Lexer

class BakingEngine:
    def __init__(self):
        self.trays = {}

    def run(self, ast):
        for node in ast:
            self.evaluate(node)

    def evaluate(self, node):
        if node.node_type == "Oven":
            self.oven_size = node.value
            print(f"Setting oven size to {self.oven_size} bits.")
        elif node.node_type == "Prepare":
            croissant = node.value['croissant']
            tray = node.value['tray']
            self.trays[tray] = croissant
            print(f"Prepared {croissant} into {tray}.")
        elif node.node_type == "Flip":
            tray = node.value['tray']
            position = node.value['position']
            self.trays[tray] = self.flip_bit(self.trays[tray], position)
            print(f"Flipped bit at {position} in {tray}. New value: {self.trays[tray]}")
        elif node.node_type == "Shift":
            tray = node.value['tray']
            direction = node.value['direction']
            steps = node.value['steps']
            self.trays[tray] = self.shift_bits(self.trays[tray], steps)
            print(f"Shifted {tray} {direction} by {steps}. New value: {self.trays[tray]}")
        elif node.node_type == "Combine":
            tray1 = node.value['tray1']
            tray2 = node.value['tray2']
            result = node.value['result']
            self.trays[result] = self.combine_trays(self.trays[tray1], self.trays[tray2])
            print(f"Combined {tray1} and {tray2} into {result}. New value: {self.trays[result]}")
        elif node.node_type == "Serve":
            print(f"Serving {self.trays[node.value]} from {node.value}.")
        elif node.node_type == "BakeLoop":
            times = node.value
            for _ in range(times):
                for child in node.children:
                    self.evaluate(child)
            print(f"Baked the croissant {times} times.")

    def flip_bit(self, croissant, position):
        croissant_list = list(croissant)
        croissant_list[position] = '1' if croissant_list[position] == '0' else '0'
        return "".join(croissant_list)

    def shift_bits(self, croissant, steps):
        return croissant[steps:] + "0" * steps

    def combine_trays(self, tray1, tray2):
        return "".join(['1' if t1 == '1' or t2 == '1' else '0' for t1, t2 in zip(tray1, tray2)])


# Sample run
if __name__ == "__main__":
    code = """
    Oven<8>
    Prepare <{{{1}{0}{1}{1}}}> into TrayA
    Prepare <{{{0}{1}{1}{0}}}> into TrayB
    Combine TrayA with TrayB into TrayC
    Flip TrayC at 2
    Serve TrayC
    Take out from oven
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    engine = BakingEngine()
    engine.run(ast)
