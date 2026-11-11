import json
import math
import os
import sys
import tempfile
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any


class EmployeeError(Exception):
    """Base exception for employee management errors."""


class EmployeeNotFoundError(EmployeeError):
    pass


class DuplicateEmployeeError(EmployeeError):
    pass


class EmployeeStorageError(EmployeeError):
    pass


@dataclass(frozen=True)
class Employee:
    employee_id: str
    name: str
    age: int
    department: str
    salary: float

    def __post_init__(self) -> None:
        for field_name in ("employee_id", "name", "department"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name.replace('_', ' ').title()} must not be empty.")
            object.__setattr__(self, field_name, value.strip())

        if isinstance(self.age, bool) or not isinstance(self.age, int) or self.age <= 0:
            raise ValueError("Age must be a positive whole number.")
        if (
            isinstance(self.salary, bool)
            or not isinstance(self.salary, (int, float))
            or not math.isfinite(self.salary)
            or self.salary < 0
        ):
            raise ValueError("Salary must be a non-negative number.")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Employee":
        required_fields = {"employee_id", "name", "age", "department", "salary"}
        if not isinstance(data, dict) or set(data) != required_fields:
            raise ValueError("Employee record has missing or unexpected fields.")
        return cls(**data)


class EmployeeManager:
    def __init__(self, storage_path: str | Path | None = None) -> None:
        self.storage_path = (
            Path(storage_path)
            if storage_path is not None
            else Path(__file__).with_name("employees.json")
        )
        self._employees = self._load()

    def _load(self) -> list[Employee]:
        if not self.storage_path.exists():
            return []

        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                raise ValueError("The JSON document must contain a list of employees.")
            employees = [Employee.from_dict(item) for item in data]
            employee_ids = [employee.employee_id for employee in employees]
            if len(employee_ids) != len(set(employee_ids)):
                raise ValueError("The JSON document contains duplicate employee IDs.")
            return employees
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
            raise EmployeeStorageError(
                f"Could not load employee records from {self.storage_path}: {error}"
            ) from error

    def _save(self, employees: list[Employee]) -> None:
        temporary_path: str | None = None
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.storage_path.parent,
                delete=False,
            ) as temporary_file:
                temporary_path = temporary_file.name
                json.dump([asdict(employee) for employee in employees], temporary_file, indent=2)
                temporary_file.write("\n")
            os.replace(temporary_path, self.storage_path)
        except (OSError, TypeError, ValueError) as error:
            raise EmployeeStorageError(
                f"Could not save employee records to {self.storage_path}: {error}"
            ) from error
        finally:
            if temporary_path is not None and os.path.exists(temporary_path):
                os.unlink(temporary_path)

    def add_employee(self, employee: Employee) -> None:
        if any(item.employee_id == employee.employee_id for item in self._employees):
            raise DuplicateEmployeeError(
                f"Employee ID '{employee.employee_id}' already exists."
            )
        updated = [*self._employees, employee]
        self._save(updated)
        self._employees = updated

    def update_employee(self, employee_id: str, **changes: Any) -> Employee:
        for index, employee in enumerate(self._employees):
            if employee.employee_id == employee_id:
                allowed_fields = {"name", "age", "department", "salary"}
                if not changes or not changes.keys() <= allowed_fields:
                    raise ValueError("Provide at least one valid employee field to update.")
                updated_employee = replace(employee, **changes)
                updated = self._employees.copy()
                updated[index] = updated_employee
                self._save(updated)
                self._employees = updated
                return updated_employee
        raise EmployeeNotFoundError(f"Employee ID '{employee_id}' was not found.")

    def delete_employee(self, employee_id: str) -> Employee:
        for index, employee in enumerate(self._employees):
            if employee.employee_id == employee_id:
                updated = self._employees.copy()
                del updated[index]
                self._save(updated)
                self._employees = updated
                return employee
        raise EmployeeNotFoundError(f"Employee ID '{employee_id}' was not found.")

    def get_employee(self, employee_id: str) -> Employee:
        for employee in self._employees:
            if employee.employee_id == employee_id:
                return employee
        raise EmployeeNotFoundError(f"Employee ID '{employee_id}' was not found.")

    def list_employees(self) -> list[Employee]:
        return self._employees.copy()


def _read_employee() -> Employee:
    return Employee(
        employee_id=input("Employee ID: ").strip(),
        name=input("Name: ").strip(),
        age=int(input("Age: ")),
        department=input("Department: ").strip(),
        salary=float(input("Salary: ")),
    )


def _update_employee(manager: EmployeeManager) -> None:
    employee_id = input("Employee ID to update: ").strip()
    current = manager.get_employee(employee_id)
    print("Press Enter to keep the current value.")

    name = input(f"Name [{current.name}]: ").strip()
    age_text = input(f"Age [{current.age}]: ").strip()
    department = input(f"Department [{current.department}]: ").strip()
    salary_text = input(f"Salary [{current.salary}]: ").strip()

    changes: dict[str, Any] = {}
    if name:
        changes["name"] = name
    if age_text:
        changes["age"] = int(age_text)
    if department:
        changes["department"] = department
    if salary_text:
        changes["salary"] = float(salary_text)

    employee = manager.update_employee(employee_id, **changes)
    print(f"Updated employee: {employee}")


def _display_employees(employees: list[Employee]) -> None:
    if not employees:
        print("No employee records found.")
        return
    for employee in employees:
        print(
            f"ID: {employee.employee_id} | Name: {employee.name} | "
            f"Age: {employee.age} | Department: {employee.department} | "
            f"Salary: {employee.salary:.2f}"
        )


def main(storage_path: str | Path | None = None) -> int:
    try:
        manager = EmployeeManager(storage_path)
    except EmployeeStorageError as error:
        print(f"Storage error: {error}", file=sys.stderr)
        return 1

    actions = {
        "1": "Add employee",
        "2": "Update employee",
        "3": "Delete employee",
        "4": "View all employees",
        "5": "View one employee",
        "0": "Exit",
    }

    while True:
        print("\nEmployee Management")
        for key, description in actions.items():
            print(f"{key}. {description}")

        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                manager.add_employee(_read_employee())
                print("Employee added.")
            elif choice == "2":
                _update_employee(manager)
            elif choice == "3":
                employee_id = input("Employee ID to delete: ").strip()
                deleted = manager.delete_employee(employee_id)
                print(f"Deleted employee: {deleted.name}")
            elif choice == "4":
                _display_employees(manager.list_employees())
            elif choice == "5":
                employee_id = input("Employee ID to view: ").strip()
                _display_employees([manager.get_employee(employee_id)])
            elif choice == "0":
                print("Goodbye.")
                return 0
            else:
                print("Please choose a listed option.")
        except (EmployeeError, ValueError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    raise SystemExit(main())
