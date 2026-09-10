"""Check the backend AST without starting Flask, importing the application, or connecting to the DB.

Run from any directory: python backend/checks/static_check.py
Ruff additionally checks for undefined variables and common Python errors.
"""

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTE_MODULES = {
    "auth": "routes.auth_routes",
    "admin": "routes.user_routes",
    "student": "routes.student_routes",
    "lecturer": "routes.teaching_routes",
}


def module_name(path):
    """Convert a Python path to a module name for internal import analysis."""
    parts = list(path.relative_to(ROOT).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def check_backend():
    """Check syntax, documentation, UML classes, route contracts, calls, and parameterized SQL."""
    errors = []
    trees = {}
    definitions = 0
    sql_count = 0
    for path in sorted(ROOT.rglob("*.py")):
        if any(
            part.startswith(".") or part == "__pycache__"
            for part in path.relative_to(ROOT).parts
        ):
            continue
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            compile(tree, str(path), "exec")
            trees[module_name(path)] = tree
        except (SyntaxError, UnicodeError) as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                definitions += 1
                if not ast.get_docstring(node):
                    errors.append(
                        f"{path.name}:{node.lineno}: missing documentation for {node.name}"
                    )
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if (
                    node.func.attr
                    in ("execute", "execute_query", "fetch_one", "fetch_all")
                    and len(node.args) >= 2
                ):
                    sql, params = node.args[:2]
                    if (
                        isinstance(sql, ast.Constant)
                        and isinstance(sql.value, str)
                        and isinstance(params, (ast.Tuple, ast.List))
                    ):
                        sql_count += 1
                        if sql.value.count("%s") != len(params.elts):
                            errors.append(
                                f"{path.name}:{node.lineno}: SQL parameter count does not match"
                            )

    classes = {}
    imports = {name: set() for name in trees}
    for name, tree in trees.items():
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                classes[node.name] = node
            if isinstance(node, ast.ImportFrom):
                if node.level:
                    parts = name.split(".")[: -node.level]
                    target = ".".join(parts + ([node.module] if node.module else []))
                else:
                    target = node.module or ""
                if target in trees:
                    imports[name].add(target)
                    exports = {
                        n.name
                        for n in trees[target].body
                        if isinstance(n, (ast.ClassDef, ast.FunctionDef))
                    }
                    exports.update(
                        t.id
                        for n in trees[target].body
                        if isinstance(n, ast.Assign)
                        for t in n.targets
                        if isinstance(t, ast.Name)
                    )
                    exports.update(
                        a.asname or a.name
                        for n in trees[target].body
                        if isinstance(n, (ast.Import, ast.ImportFrom))
                        for a in n.names
                    )
                    for alias in node.names:
                        if alias.name != "*" and alias.name not in exports:
                            errors.append(
                                f"{name}: import {alias.name} does not exist in {target}"
                            )
                elif node.level:
                    errors.append(f"{name}: relative module does not exist: {target}")
                if name.startswith("models.") and target in (
                    "flask",
                    "http_support",
                    "security",
                ):
                    errors.append(f"{name}: business logic depends on HTTP layer {target}")

    visited = set()

    def visit(name, stack):
        """Traverse the internal import graph to detect circular dependencies."""
        if name in stack:
            errors.append("Circular import: " + " -> ".join(stack + [name]))
            return
        if name in visited:
            return
        for target in imports[name]:
            visit(target, stack + [name])
        visited.add(name)

    for name in imports:
        visit(name, [])

    expected = {
        "User": {"login", "viewAccountInfo", "changePassword", "logout"},
        "Student": {
            "viewCourses",
            "registerCourse",
            "dropCourse",
            "viewRegistrationStatus",
            "viewGrades",
        },
        "Lecturer": {
            "viewTeachingCourse",
            "viewRegisteredStudents",
            "manageStudentGrade",
        },
        "Administrator": {
            "manageStudent",
            "manageLecturer",
            "manageMajor",
            "manageCurriculum",
            "manageCourse",
            "manageSemester",
            "manageRegistrationPeriod",
            "generateRegistrationDemandReport",
            "assignLecturer",
        },
        "Course": {"checkPrerequisite", "checkCapacity"},
        "Semester": {"checkOverlap"},
        "Major": set(),
        "TeachingAssignment": set(),
        "RegistrationPeriod": {"updateRegistrationStatus"},
        "Registration": {"saveRegistration", "updateRegistrationStatus"},
        "GradeRecord": {"calculateResultStatus"},
    }
    for name, methods in expected.items():
        cls = classes.get(name)
        if cls is None:
            errors.append(f"Missing UML class {name}")
            continue
        actual = {n.name for n in cls.body if isinstance(n, ast.FunctionDef)}
        if methods - actual:
            errors.append(f"{name}: missing method {sorted(methods - actual)}")
        if name in ("Student", "Lecturer", "Administrator") and "User" not in [
            ast.unparse(b) for b in cls.bases
        ]:
            errors.append(f"{name}: does not inherit from User")

    contract = json.loads(
        (ROOT / "checks/route_contract.json").read_text(encoding="utf-8")
    )
    for entry in contract:
        route_module_name = ROUTE_MODULES.get(entry["module"], entry["module"])
        funcs = {
            n.name: n
            for n in trees[route_module_name].body
            if isinstance(n, ast.FunctionDef)
        }
        func = funcs.get(entry["name"])
        if func is None:
            errors.append(f"Missing API {entry['module']}.{entry['name']}")
            continue
        if [ast.unparse(d) for d in func.decorator_list] != entry[
            "decorators"
        ] or ast.unparse(func.args) != entry["args"]:
            errors.append(
                f"Changed route/permission/parameters: {entry['module']}.{entry['name']}"
            )

    routed_calls = 0
    for module in ROUTE_MODULES.values():
        for func in trees[module].body:
            if not isinstance(func, ast.FunctionDef):
                continue

            # Record examples such as: student = Student(current_user).
            objects = {}
            for statement in func.body:
                if not isinstance(statement, ast.Assign):
                    continue
                value = statement.value
                if not isinstance(value, ast.Call) or not isinstance(
                    value.func, ast.Name
                ):
                    continue
                if value.func.id in classes:
                    for target in statement.targets:
                        if isinstance(target, ast.Name):
                            objects[target.id] = value.func.id

            calls_in_route = 0
            for node in ast.walk(func):
                if not isinstance(node, ast.Call) or not isinstance(
                    node.func, ast.Attribute
                ):
                    continue
                owner = node.func.value
                if not isinstance(owner, ast.Name) or owner.id not in objects:
                    continue
                class_name = objects[owner.id]
                cls = classes[class_name]
                methods = {
                    n.name: n for n in cls.body if isinstance(n, ast.FunctionDef)
                }
                method = methods.get(node.func.attr)
                if method is None:
                    errors.append(
                        f"{module}: method does not exist {class_name}.{node.func.attr}"
                    )
                    continue

                calls_in_route += 1
                routed_calls += 1
                parameters = [argument.arg for argument in method.args.args[1:]]
                keyword_only = [argument.arg for argument in method.args.kwonlyargs]
                positional_names = set(parameters[: len(node.args)])
                keyword_names = {keyword.arg for keyword in node.keywords}
                allowed = set(parameters + keyword_only)
                required_count = len(parameters) - len(method.args.defaults)
                required = set(parameters[:required_count])
                for argument, default in zip(method.args.kwonlyargs, method.args.kw_defaults):
                    if default is None:
                        required.add(argument.arg)
                supplied = positional_names | keyword_names
                if (
                    len(node.args) > len(parameters)
                    or positional_names & keyword_names
                    or not required <= supplied
                    or not supplied <= allowed
                ):
                    errors.append(f"{module}: incorrect arguments for {method.name}")

            if calls_in_route == 0:
                errors.append(
                    f"{module}.{func.name}: business-object call not found"
                )

    print(f"Python files: {len(trees)}; documented classes/functions: {definitions}")
    print(
        f"UML classes: {len(expected)}; original routes preserved: {len(contract)}; routed method signatures: {routed_calls}; SQL parameter checks: {sql_count}"
    )
    for error in errors:
        print("FAIL:", error)
    print("STATIC CHECK: " + ("FAIL" if errors else "PASS"))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(check_backend())
