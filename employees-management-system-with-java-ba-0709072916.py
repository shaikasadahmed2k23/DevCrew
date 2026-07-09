import requests
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

@dataclass
class Employee:
    """
    Represents an employee in the system.

    Attributes:
        id (str): Unique identifier for the employee, assigned by the backend.
        first_name (str): Employee's first name.
        last_name (str): Employee's last name.
        email (str): Employee's email address (typically unique).
        position (str): Employee's job position.
        hire_date (str): Date the employee was hired, in 'YYYY-MM-DD' format.
        salary (float): Employee's annual salary.
    """
    id: str
    first_name: str
    last_name: str
    email: str
    position: str
    hire_date: str
    salary: float

class EmployeeManagementError(Exception):
    """Base exception for all employee management system client errors."""
    pass

class EmployeeNotFoundError(EmployeeManagementError):
    """Raised when an employee with a given ID is not found (HTTP 404)."""
    pass

class EmployeeConflictError(EmployeeManagementError):
    """Raised when an operation would lead to a conflict (e.g., duplicate email) (HTTP 409)."""
    pass

class BackendConnectionError(EmployeeManagementError):
    """Raised when the client cannot establish a connection to the backend service."""
    pass

class BackendServiceError(EmployeeManagementError):
    """Raised for unexpected errors from the backend service (e.g., 4xx or 5xx status codes not specifically handled)."""
    pass

class EmployeeManagementClient:
    """
    Client for interacting with a Java-based Employees Management System backend.

    This client facilitates CRUD operations (Create, Read, Update, Delete)
    on employee data through a RESTful API. It is designed to be robust by
    handling network communication issues, various HTTP error responses,
    and data serialization/deserialization.
    """

    def __init__(self, base_url: str):
        """
        Initializes the EmployeeManagementClient.

        Args:
            base_url (str): The base URL of the Java backend's API endpoint for employees.
                            Example: "http://localhost:8080/api" or "https://api.example.com/employees"
                            Ensure the URL points to the root of the API resources.
        """
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self._session = requests.Session()
        # You might add default headers here for authentication, content type, etc.
        # self._session.headers.update({'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Internal helper method to execute HTTP requests to the backend API.

        Args:
            method (str): The HTTP method to use (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            endpoint (str): The API endpoint relative to the base URL (e.g., 'employees' or 'employees/123').
            data (Optional[Dict[str, Any]]): A dictionary representing the JSON payload for
                                            'POST' or 'PUT' requests.

        Returns:
            Optional[Dict[str, Any]]: The JSON response body as a dictionary if the request
                                      was successful and contained content. Returns None for
                                      successful requests with no content (e.g., 204 No Content).

        Raises:
            BackendConnectionError: If a network error prevents connection to the backend.
            EmployeeNotFoundError: If the requested resource is not found (HTTP 404).
            EmployeeConflictError: If the request conflicts with existing data (HTTP 409).
            BackendServiceError: For other HTTP client (4xx) or server (5xx) errors.
            EmployeeManagementError: For any other unexpected errors during the request process.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            if method in ['POST', 'PUT']:
                response = self._session.request(method, url, json=data, timeout=10)
            else:
                response = self._session.request(method, url, timeout=10)

            response.raise_for_status()  # Raises HTTPError for 4xx or 5xx responses

            if response.status_code == 204: # No Content
                return None
            return response.json()

        except requests.exceptions.ConnectionError as e:
            raise BackendConnectionError(f"Failed to connect to backend at {self.base_url}: {e}")
        except requests.exceptions.Timeout as e:
            raise BackendConnectionError(f"Request to backend timed out: {e}")
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else 0
            error_detail = e.response.text if e.response is not None else "No response body"
            if status_code == 404:
                raise EmployeeNotFoundError(f"Resource not found at {url}. Details: {error_detail}")
            elif status_code == 409:
                raise EmployeeConflictError(f"Conflict occurred at {url}. Details: {error_detail}")
            elif 400 <= status_code < 500:
                raise BackendServiceError(f"Client error ({status_code}) from backend: {error_detail}")
            elif 500 <= status_code < 600:
                raise BackendServiceError(f"Server error ({status_code}) from backend: {error_detail}")
            raise BackendServiceError(f"An unexpected HTTP error occurred: {e}")
        except Exception as e:
            raise EmployeeManagementError(f"An unexpected error occurred during API request: {e}")

    def add_employee(self, employee_data: Dict[str, Any]) -> Optional[Employee]:
        """
        Adds a new employee to the system.

        Args:
            employee_data (Dict[str, Any]): A dictionary containing the new employee's details.
                                         The 'id' field should not be included as it's
                                         generated by the backend.
                                         Example: {'first_name': 'John', 'last_name': 'Doe',
                                                   'email': 'john.doe@example.com', 'position': 'Dev',
                                                   'hire_date': '2023-01-01', 'salary': 75000.0}

        Returns:
            Optional[Employee]: The created Employee object with its backend-assigned ID,
                                or None if the operation failed.

        Raises:
            EmployeeConflictError: If an employee with the same unique identifier (e.g., email) already exists.
            BackendServiceError: For other backend-related errors.
            BackendConnectionError: If the backend is unreachable.
        """
        # Ensure 'id' is not sent during creation as it's typically auto-generated
        if 'id' in employee_data:
            employee_data = {k: v for k, v in employee_data.items() if k != 'id'}

        response_data = self._request('POST', 'employees', data=employee_data)
        if response_data:
            return Employee(**response_data)
        return None

    def get_employee(self, employee_id: str) -> Optional[Employee]:
        """
        Retrieves an employee by their unique ID.

        Args:
            employee_id (str): The unique ID of the employee to retrieve.

        Returns:
            Optional[Employee]: The Employee object if found, otherwise None.

        Raises:
            BackendServiceError: For backend-related errors.
            BackendConnectionError: If the backend is unreachable.
        """
        try:
            response_data = self._request('GET', f'employees/{employee_id}')
            if response_data:
                return Employee(**response_data)
            return None
        except EmployeeNotFoundError:
            return None # Return None if not found, rather than re-raising for client convenience

    def update_employee(self, employee_id: str, updates: Dict[str, Any]) -> Optional[Employee]:
        """
        Updates specific details of an existing employee.

        Args:
            employee_id (str): The ID of the employee to update.
            updates (Dict[str, Any]): A dictionary containing the fields to update and their new values.
                                   Example: {'position': 'Senior Developer', 'salary': 100000.0}
                                   The 'id' field in updates will be ignored.

        Returns:
            Optional[Employee]: The updated Employee object, or None if the update failed or employee not found.

        Raises:
            EmployeeNotFoundError: If no employee with the given ID exists.
            EmployeeConflictError: If an update (e.g., changing email to an existing one) causes a conflict.
            BackendServiceError: For other backend-related errors.
            BackendConnectionError: If the backend is unreachable.
        """
        # Ensure 'id' is not sent in the update payload
        if 'id' in updates:
            updates = {k: v for k, v in updates.items() if k != 'id'}

        response_data = self._request('PUT', f'employees/{employee_id}', data=updates)
        if response_data:
            return Employee(**response_data)
        return None

    def delete_employee(self, employee_id: str) -> bool:
        """
        Deletes an employee from the system by their ID.

        Args:
            employee_id (str): The ID of the employee to delete.

        Returns:
            bool: True if the employee was successfully deleted, False if the employee
                  was not found or deletion failed for other specific reasons.

        Raises:
            BackendServiceError: For backend-related errors not related to not found.
            BackendConnectionError: If the backend is unreachable.
        """
        try:
            self._request('DELETE', f'employees/{employee_id}')
            return True
        except EmployeeNotFoundError:
            return False # Employee not found means no deletion occurred, so return False
        except Exception:
            raise # Re-raise other exceptions for detailed handling upstream

    def list_employees(self) -> List[Employee]:
        """
        Retrieves a list of all employees in the system.

        Returns:
            List[Employee]: A list of Employee objects. Returns an empty list if no employees
                            are found or an error occurs (after handling via exceptions).

        Raises:
            BackendServiceError: For backend-related errors.
            BackendConnectionError: If the backend is unreachable.
        """
        response_data = self._request('GET', 'employees')
        if response_data and isinstance(response_data, list):
            return [Employee(**item) for item in response_data]
        return []

# --- Example Test Cases (as comments) ---
# To run these tests, you would typically need a running Java backend
# that exposes a REST API at the specified base_url (e.g., http://localhost:8080/api).
# The backend should implement endpoints like:
# - POST /api/employees (creates an employee, returns 201 Created with employee data)
# - GET /api/employees/{id} (returns 200 OK with employee data, or 404 Not Found)
# - PUT /api/employees/{id} (updates an employee, returns 200 OK with updated employee data, or 404)
# - DELETE /api/employees/{id} (returns 204 No Content or 404 Not Found)
# - GET /api/employees (returns 200 OK with a list of employee data, or empty list)

"""
# Example Test Cases (requires a running backend at MOCK_SERVER_URL)

# MOCK_SERVER_URL = "http://localhost:8080/api" # Replace with your actual backend API base URL

# if __name__ == "__main__":
#     print("--- Running Employee Management Client Test Cases ---")
#     client = EmployeeManagementClient(base_url=MOCK_SERVER_URL)
#     test_employee_id: Optional[str] = None

#     try:
#         # Test Case 1: Add a new employee
#         print("\nTest Case 1: Adding a new employee...")
#         new_employee_data = {
#             'first_name': 'Carlos',
#             'last_name': 'Ruiz',
#             'email': 'carlos.ruiz@example.com',
#             'position': 'Data Scientist',
#             'hire_date': '2022-11-01',
#             'salary': 95000.0
#         }
#         created_employee = client.add_employee(new_employee_data)
#         if created_employee:
#             print(f"Successfully added employee: {created_employee}")
#             test_employee_id = created_employee.id
#             assert created_employee.first_name == 'Carlos'
#             print("Test Case 1 PASSED.")
#         else:
#             print("Test Case 1 FAILED: Failed to create employee.")

#         # Test Case 2: Get the created employee by ID
#         if test_employee_id:
#             print(f"\nTest Case 2: Getting employee with ID {test_employee_id}...")
#             fetched_employee = client.get_employee(test_employee_id)
#             if fetched_employee:
#                 print(f"Successfully fetched employee: {fetched_employee}")
#                 assert fetched_employee.id == test_employee_id
#                 assert fetched_employee.email == 'carlos.ruiz@example.com'
#                 print("Test Case 2 PASSED.")
#             else:
#                 print(f"Test Case 2 FAILED: Employee with ID {test_employee_id} not found.")

#         # Test Case 3: Update the employee's position and salary
#         if test_employee_id:
#             print(f"\nTest Case 3: Updating employee with ID {test_employee_id}...")
#             updates = {'position': 'Senior Data Scientist', 'salary': 110000.0}
#             updated_employee = client.update_employee(test_employee_id, updates)
#             if updated_employee:
#                 print(f"Successfully updated employee: {updated_employee}")
#                 assert updated_employee.position == 'Senior Data Scientist'
#                 assert updated_employee.salary == 110000.0
#                 print("Test Case 3 PASSED.")
#             else:
#                 print(f"Test Case 3 FAILED: Failed to update employee with ID {test_employee_id}.")

#         # Clean up: Delete the employee created during tests (optional, but good practice)
#         if test_employee_id:
#             print(f"\nCleaning up: Deleting employee with ID {test_employee_id}...")
#             if client.delete_employee(test_employee_id):
#                 print(f"Successfully deleted employee {test_employee_id}.")
#             else:
#                 print(f"Failed to delete employee {test_employee_id}.")


#     except EmployeeManagementError as e:
#         print(f"\nAn EmployeeManagementError occurred: {e}")
#     except Exception as e:
#         print(f"\nAn unexpected error occurred: {e}")

#     print("\n--- End of Test Cases ---")
"""