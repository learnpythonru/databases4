import csv
from datetime import date, timedelta
import random

from models import Company


def get_project_name():
    projects = ['Ребрендинг', 'Разработка CRM', 'Обслуживание 1С', 'Разработка сайта',
                'Опрос покупателей', 'Запуск колцентра', 'Модернизация wifi-сети',
                'Проведение исследований', 'Дизайн сайта', 'Разработка моб. приложения',
                'Дизайн буклетов', 'Аудит информационной безопасности',
                'Обучение сотрудников']

    return random.choice(projects)


def projects_for_employee(company_id, employee_id):
    projects = []
    for month in range(1, 13):
        date_start = date(2020, month, random.randint(1, 10))
        date_end = date_start + timedelta(days=random.randint(5, 20))
        project = [get_project_name(), company_id, employee_id, date_start, date_end]
        projects.append(project)
    return projects


def fake_project_list():
    data = []
    companies = Company.query.all()
    for company in companies:
        for employee in company.employees:
            data += projects_for_employee(company.id, employee.id)
    return data


def generate_data(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    generate_data(fake_project_list(), 'projects.csv')
