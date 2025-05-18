# <...> Raanzor Obfuscation
# If you want to use this obfuscation in your projects, please put this url or credit it.
# https://github.com/dsckazam/RaanzorOBFU


import ast
import base64
import random
import string
import zlib

class RaanzorObfuscator:
    def __init__(self, code, output_path):
        self.code = code
        self.output_path = output_path
        self.var_names = {}
        self.func_names = {}

    def generate_random_name(self):
        length = random.randint(10, 20)
        # Ensure the name starts with a letter
        first_char = random.choice(string.ascii_lowercase)
        remaining_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length-1))
        return first_char + remaining_chars

    def obfuscate_string(self, node):
        if isinstance(node, ast.Str):
            encoded = base64.b64encode(node.s.encode()).decode()
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='__import__', ctx=ast.Load()),
                    attr='b64decode',
                    ctx=ast.Load()
                ),
                args=[ast.Str(s=encoded)],
                keywords=[]
            )
        return node

    def obfuscate_variable_names(self, node):
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                if node.id not in self.var_names:
                    self.var_names[node.id] = self.generate_random_name()
                node.id = self.var_names[node.id]
            elif isinstance(node.ctx, ast.Load) and node.id in self.var_names:
                node.id = self.var_names[node.id]
        return node

    def obfuscate_function_names(self, node):
        if isinstance(node, ast.FunctionDef):
            if node.name not in self.func_names:
                self.func_names[node.name] = self.generate_random_name()
            node.name = self.func_names[node.name]
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in self.func_names:
            node.func.id = self.func_names[node.func.id]
        return node

    def obfuscate(self):
        tree = ast.parse(self.code)

        for node in ast.walk(tree):
            self.obfuscate_variable_names(node)
            self.obfuscate_function_names(node)
            self.obfuscate_string(node)

        obfuscated_code = ast.unparse(tree)

        compressed_code = zlib.compress(obfuscated_code.encode('utf-8'))
        encoded_code = base64.b64encode(compressed_code).decode('utf-8')

        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(f"""
import base64
import zlib

compressed_code = base64.b64decode('{encoded_code}')
decompressed_code = zlib.decompress(compressed_code).decode('utf-8')

exec(decompressed_code)
""")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python raanzor_obfuscator.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    obfuscator = RaanzorObfuscator(code, output_file)
    obfuscator.obfuscate()
    print(f"Obfuscated code saved to {output_file}")
