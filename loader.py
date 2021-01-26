import csv
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from db import db_session
from models import Project, ProjectEmployee


def prepare_data(row):
    row['company_id'] = int(row['company_id'])
    row['employee_id'] = int(row['employee_id'])
    row['date_start'] = datetime.strptime(row['date_start'], '%Y-%m-%d')
    row['date_end'] = datetime.strptime(row['date_end'], '%Y-%m-%d')
    return row


def get_or_create_project(project_name, company_id):
    project = Project.query.filter(
        Project.name == project_name, Project.company_id == company_id
    ).first()
    if not project:
        project = Project(name=project_name, company_id=company_id)
        db_session.add(project)
        try:
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise
    return project


def create_project_employee(row, project):
    project_employee = ProjectEmployee(
        employee_id=row['employee_id'],
        project_id=project.id,
        date_start=row['date_start'],
        date_end=row['date_end']
    )
    db_session.add(project_employee)
    try:
        db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        raise


def process_row(row):
    row = prepare_data(row)
    project = get_or_create_project(row['project_name'], row['company_id'])
    create_project_employee(row, project)


def print_error(row_num, error_text, exception):
    print(f"Ошибка на строке {row_num}")
    print(error_text.format(exception))
    print('-' * 100)


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['project_name',  'company_id', 'employee_id', 'date_start', 'date_end']
        reader = csv.DictReader(f, fields, delimiter=';')
        for row_num, row in enumerate(reader, start=1):
            try:
                process_row(row)
            except (TypeError, ValueError) as e:
                print_error(row_num, "Неправильный формат данных {}", e)
            except SQLAlchemyError as e:
                print_error(row_num, "Ошибка целостности данных {}", e)


if __name__ == '__main__':
    read_csv('projects.csv')
