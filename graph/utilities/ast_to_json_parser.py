import ast
import json
import pandas as pd
import yaml

class CodeEntityExtractor(ast.NodeVisitor):
    def __init__(self, file_name=None, code_lines=None):
        self.file_name = file_name
        self.code_lines = code_lines
        self.classes = []
        self.functions = []
        self.calls = []
        self.current_class = None
        self.current_function = None

    def get_signature(self, node):
        args = []
        defaults = []
        if hasattr(node, 'args'):
            for arg in node.args.args:
                args.append(arg.arg)
            if hasattr(node.args, 'defaults'):
                for default in node.args.defaults:
                    defaults.append(ast.unparse(default) if hasattr(ast, 'unparse') else None)
        return {
            'args': args,
            'defaults': defaults
        }

    def get_decorators(self, node):
        decorators = []
        if hasattr(node, 'decorator_list'):
            for dec in node.decorator_list:
                if hasattr(ast, 'unparse'):
                    decorators.append(ast.unparse(dec))
                else:
                    if isinstance(dec, ast.Name):
                        decorators.append(dec.id)
                    elif isinstance(dec, ast.Attribute):
                        decorators.append(dec.attr)
        return decorators

    def get_inheritances(self, node):
        bases = []
        if hasattr(node, 'bases'):
            for base in node.bases:
                if hasattr(ast, 'unparse'):
                    bases.append(ast.unparse(base))
                else:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        bases.append(base.attr)
        return bases

    def visit_ClassDef(self, node):
        class_info = {
            'name': node.name,
            'methods': [],
            'decorators': self.get_decorators(node),
            'inheritances': self.get_inheritances(node)
        }
        self.classes.append(class_info)
        self.current_class = node.name
        for n in node.body:
            if isinstance(n, ast.FunctionDef):
                method_content = None
                if hasattr(n, 'lineno') and hasattr(n, 'end_lineno') and self.code_lines:
                    method_content = '\n'.join(self.code_lines[n.lineno-1:n.end_lineno])
                signature = self.get_signature(n)
                decorators = self.get_decorators(n)
                class_info['methods'].append({'name': n.name, 'content': method_content, 'signature': signature, 'decorators': decorators})
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class:
            pass
        else:
            func_content = None
            if hasattr(node, 'lineno') and hasattr(node, 'end_lineno') and self.code_lines:
                func_content = '\n'.join(self.code_lines[node.lineno-1:node.end_lineno])
            signature = self.get_signature(node)
            decorators = self.get_decorators(node)
            self.functions.append({'name': node.name, 'content': func_content, 'signature': signature, 'decorators': decorators})
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        called_func = None
        if isinstance(node.func, ast.Name):
            called_func = node.func.id
        elif isinstance(node.func, ast.Attribute):
            called_func = node.func.attr
        if called_func and self.current_function:
            self.calls.append({
                'caller_function': self.current_function,
                'caller_class': self.current_class,
                'called_function': called_func
            })
        self.generic_visit(node)

    def get_imports(self, tree, project_modules=None):
        import sys
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        result = []
        builtin_modules = set(sys.builtin_module_names)
        project_modules = set(project_modules or [])
        for imp in imports:
            if imp in builtin_modules:
                result.append({'module': imp, 'type': 'external_builtin'})
            elif imp in project_modules:
                result.append({'module': imp, 'type': 'internal'})
            else:
                result.append({'module': imp, 'type': 'external'})
        return result

def parse_parquet_to_json(parquet_path, output_path, cross_calls=False):
    df = pd.read_parquet(parquet_path)
    all_results = []
    function_index = {} if cross_calls else None
    method_index = {} if cross_calls else None

    project_modules = set(df[0].apply(lambda x: str(x).replace('.py', '').replace('/', '.').split('.')[-1]) if 0 in df.columns else [])
    for _, row in df.iterrows():
        file_path = row[0] if 0 in row else row.get('name', None)
        code_content = row[1] if 1 in row else row.get('content', None)
        if file_path is None or code_content is None:
            continue

        # Skip README files
        if str(file_path).lower().startswith('readme'):
            continue

        # Handle Python files
        if str(file_path).endswith('.py'):
            try:
                tree = ast.parse(code_content)
                extractor = CodeEntityExtractor(file_name=str(file_path), code_lines=code_content.splitlines())
                extractor.visit(tree)
                imports = extractor.get_imports(tree, project_modules=project_modules)
                result = {
                    'file': str(file_path),
                    'type': 'python',
                    'imports': imports,
                    'classes': extractor.classes,
                    'functions': extractor.functions,
                    'calls': extractor.calls
                }
                if cross_calls:
                    for func in extractor.functions:
                        function_index.setdefault(func['name'], []).append(str(file_path))
                    for cls in extractor.classes:
                        for method in cls['methods']:
                            method_index.setdefault((cls['name'], method['name']), []).append(str(file_path))
                    result['methods'] = [m for cls in extractor.classes for m in cls['methods']]
                all_results.append(result)
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")

        # Handle Markdown files
        elif str(file_path).endswith('.md'):
            try:
                result = {
                    'file': str(file_path),
                    'type': 'markdown',
                    'content': code_content
                }
                all_results.append(result)
            except Exception as e:
                print(f"Error processing Markdown file {file_path}: {e}")

        # Handle Text files
        elif str(file_path).endswith('.txt'):
            try:
                result = {
                    'file': str(file_path),
                    'type': 'text',
                    'content': code_content
                }
                all_results.append(result)
            except Exception as e:
                print(f"Error processing Text file {file_path}: {e}")

        # Handle YAML files
        elif str(file_path).endswith(('.yaml', '.yml')):
            try:
                yaml_content = yaml.safe_load(code_content)
                result = {
                    'file': str(file_path),
                    'type': 'yaml',
                    'content': yaml_content
                }
                all_results.append(result)
            except Exception as e:
                print(f"Error processing YAML file {file_path}: {e}")

    if cross_calls:
        for result in all_results:
            if result['type'] == 'python':
                for call in result['calls']:
                    called_func = call['called_function']
                    caller_class = call['caller_class']
                    caller_file = result['file']
                    called_files = function_index.get(called_func, [])
                    called_method_files = []
                    if caller_class:
                        called_method_files = method_index.get((caller_class, called_func), [])
                    call['called_function_files'] = called_files
                    call['called_method_files'] = called_method_files
                    call['self_call_function'] = caller_file in called_files
                    call['self_call_method'] = caller_file in called_method_files

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
