import json
import tempfile
import unittest
from pathlib import Path

from employee_management import (
    DuplicateEmployeeError,
    Employee,
    EmployeeManager,
    EmployeeNotFoundError,
    EmployeeStorageError,
)


class EmployeeManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name) / "employees.json"
        self.manager = EmployeeManager(self.storage_path)
        self.employee = Employee("E001", "Alex Smith", 30, "Engineering", 75000.0)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_and_reload_employee(self) -> None:
        self.manager.add_employee(self.employee)

        reloaded = EmployeeManager(self.storage_path)
        self.assertEqual(reloaded.get_employee("E001"), self.employee)
        self.assertEqual(
            json.loads(self.storage_path.read_text(encoding="utf-8"))[0]["name"],
            "Alex Smith",
        )

    def test_update_employee_persists_changes(self) -> None:
        self.manager.add_employee(self.employee)

        updated = self.manager.update_employee("E001", department="Research", salary=80000)

        self.assertEqual(updated.department, "Research")
        self.assertEqual(EmployeeManager(self.storage_path).get_employee("E001"), updated)

    def test_delete_employee_persists_removal(self) -> None:
        self.manager.add_employee(self.employee)

        deleted = self.manager.delete_employee("E001")

        self.assertEqual(deleted, self.employee)
        self.assertEqual(EmployeeManager(self.storage_path).list_employees(), [])

    def test_duplicate_and_missing_employee_errors(self) -> None:
        self.manager.add_employee(self.employee)

        with self.assertRaises(DuplicateEmployeeError):
            self.manager.add_employee(self.employee)
        with self.assertRaises(EmployeeNotFoundError):
            self.manager.delete_employee("missing")

    def test_invalid_json_raises_storage_error(self) -> None:
        self.storage_path.write_text("{invalid", encoding="utf-8")

        with self.assertRaises(EmployeeStorageError):
            EmployeeManager(self.storage_path)

    def test_non_finite_salary_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Employee("E002", "Jamie Jones", 25, "Sales", float("nan"))


if __name__ == "__main__":
    unittest.main()
