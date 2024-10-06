import argparse
import sys
from croisslang.lexer import Lexer
from croisslang.parser import Parser
from croisslang.baking_engine import BakingEngine

def run_croisslang(file_path):
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        engine = BakingEngine()
        engine.run(ast)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running croisslang: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Run a Croisslang (.crois) script.")
    parser.add_argument('file', help="Path to the .crois file")
    args = parser.parse_args()

    if not args.file.endswith('.crois'):
        print("Error: Input file must have a .crois extension.")
        sys.exit(1)

    run_croisslang(args.file)

if __name__ == "__main__":
    main()
