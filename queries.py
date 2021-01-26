from sqlalchemy import func

from db import db_session
from models import Project, Company, ProjectEmployee, Employee


def company_projects_employees(company_name):
    query = Project.query.join(
        Project.company, Project.employees
    ).filter(Company.name == company_name)

    for project in query:
        print('-' * 20)
        print(project.name)
        for project_employee in project.employees:
            delta = (project_employee.date_end - project_employee.date_start).days
            print(f"{project_employee.employee.name} -- {delta}")


def project_time_total(company_name):
    query = db_session.query(
        Project.name,
        func.sum(ProjectEmployee.date_end - ProjectEmployee.date_start)
    ).join(
        Project.company, Project.employees
    ).filter(Company.name == company_name).group_by(Project.name)

    for project_name, delta in query:
        print(f"{project_name} -- {delta}")


def project_employees_time_total(company_name):
    query = db_session.query(
        Project.name,
        Employee.name,
        func.sum(ProjectEmployee.date_end - ProjectEmployee.date_start)
    ).join(
        Project.company, Project.employees, ProjectEmployee.employee
    ).filter(Company.name == company_name).group_by(Project.name, Employee.name)

    for project_name, employee_name, delta in query:
        print(f"{project_name} -- {employee_name} -- {delta}")


if __name__ == '__main__':
    # company_projects_employees('Метро Кэш энд Керри (Metro Cash & Carry)')
    # project_time_total('Метро Кэш энд Керри (Metro Cash & Carry)')
    project_employees_time_total('Метро Кэш энд Керри (Metro Cash & Carry)')
