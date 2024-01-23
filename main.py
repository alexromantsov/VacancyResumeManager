import json
import os
import pandas as pd

from openai import OpenAI

API_KEY = ''


class VacanciesDB:
    def __init__(self):
        """ Инициализация базы данных вакансий. """
        self.data = pd.DataFrame(columns=["ID", "Название вакансии", "Описание", "Требования"])

    def add_vacancy(self, title, description, requirements, **kwargs):
        new_id = (self.data['ID'].max() + 1) if not self.data.empty else 1
        vacancy = pd.DataFrame(
            [{"ID": new_id, "Название вакансии": title, "Описание": description, "Требования": requirements}])
        self.data = pd.concat([self.data, vacancy], ignore_index=True)

    def get_vacancies(self):
        return self.data
    def update_vacancy(self, id, updated_data):
        self.data.loc[self.data['ID'] == id, list(updated_data.keys())] = list(updated_data.values())

    def delete_vacancy(self, id):
        self.data = self.data[self.data['ID'] != id]


class ResumesDB:
    def __init__(self):
        self.data = pd.DataFrame(columns=["ID", "Навыки", "Опыт работы"])

    def add_resume(self, skills, experience, **kwargs):
        new_id = (self.data['ID'].max() + 1) if not self.data.empty else 1
        resume = pd.DataFrame([{"ID": new_id, "Навыки": skills, "Опыт работы": experience}])
        self.data = pd.concat([self.data, resume], ignore_index=True)

    def get_resumes(self):
        return self.data

    def update_resume(self, id, updated_data):

        self.data.loc[self.data['ID'] == id, list(updated_data.keys())] = list(updated_data.values())

    def delete_resume(self, id):
        self.data = self.data[self.data['ID'] != id]


class XLSManager:
    def __init__(self, vacancies_file="vacancies.xlsx", resumes_file="resumes.xlsx"):
        self.vacancies_file = vacancies_file
        self.resumes_file = resumes_file
        self.vacancies_db = VacanciesDB()
        self.resumes_db = ResumesDB()
        self.load_data()

    def check_and_create_file(self, file_path):
        if not os.path.exists(file_path):
            data = pd.DataFrame()
            data.to_excel(file_path)

    def load_data(self):
        """ Загрузка данных из файлов в объекты баз данных. """
        if os.path.exists(self.vacancies_file):
            self.vacancies_db.data = pd.read_excel(self.vacancies_file)
        if os.path.exists(self.resumes_file):
            self.resumes_db.data = pd.read_excel(self.resumes_file)

    def save_data(self):
        self.vacancies_db.data.to_excel(self.vacancies_file, index=False)
        self.resumes_db.data.to_excel(self.resumes_file, index=False)

    def generate_and_add_record(self, record_type, name):
        """
        Генерация и добавление записи (вакансии или резюме) с помощью GPT API.
        """
        client = OpenAI(api_key=API_KEY)

        if record_type == 'vacancy':
            prompt_message = f"Сгенерируй описание для вакансии '{name}'" + "в формате json {{'ID': id, 'title': title, 'description': description, 'requirements': requirements}}."
        elif record_type == 'resume':
            prompt_message = f"Сгенерируй описание для резюме '{name}'" + "в формате json {{'ID': id, 'skills': skills, 'experience': experience}}."
        else:
            raise ValueError("Неверный тип записи")

        # Создание запроса к GPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            temperature=0.8,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt_message}
            ]
        )
        try:
            generated_data = json.loads(response.choices[0].message.content)
            # print(generated_data)

            if record_type == 'vacancy':
                self.vacancies_db.add_vacancy(**generated_data)
            elif record_type == 'resume':
                self.resumes_db.add_resume(**generated_data)

            self.save_data()

        except json.JSONDecodeError:
            print("Ответ получен не в JSON формате.")

    def auto_generate_records(self):
        vacancy_names = ["Разработчик Python", "Аналитик данных", "Проектный менеджер", "Тестировщик ПО",
                         "Web-разработчик"]
        resume_names = ["Python, Django", "SQL, Анализ данных", "Управление проектами, Agile", "Тестирование ПО, QA",
                        "HTML, CSS, JavaScript"]

        for name in vacancy_names:
            self.generate_and_add_record(record_type="vacancy", name=name)
        for name in resume_names:
            self.generate_and_add_record(record_type="resume", name=name)

        self.save_data()


if __name__ == "__main__":
    manager = XLSManager()

    while True:
        print("\nВыберите действие:")
        print("1 - Показать все вакансии")
        print("2 - Показать все резюме")
        print("3 - Добавить вакансию")
        print("4 - Добавить резюме")
        print("5 - Удалить вакансию")
        print("6 - Удалить резюме")
        print("7 - Автоматически сгенерировать вакансии и резюме")
        print("8 - Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            print(manager.vacancies_db.get_vacancies())
        elif choice == '2':
            print(manager.resumes_db.get_resumes())
        elif choice == '3':
            title = input("Введите название вакансии: ")
            description = input("Введите описание вакансии: ")
            requirements = input("Введите требования вакансии: ")
            manager.vacancies_db.add_vacancy(title, description, requirements)
            manager.save_data()
        elif choice == '4':
            skills = input("Введите навыки: ")
            experience = input("Введите опыт работы: ")
            manager.resumes_db.add_resume(skills, experience)
            manager.save_data()
        elif choice == '5':
            vacancy_id = int(input("Введите ID вакансии для удаления: "))
            manager.vacancies_db.delete_vacancy(vacancy_id)
            manager.save_data()
        elif choice == '6':
            resume_id = int(input("Введите ID резюме для удаления: "))
            manager.resumes_db.delete_resume(resume_id)
            manager.save_data()
        elif choice == '7':
            manager.auto_generate_records()
            print("Вакансии и резюме успешно сгенерированы.")
        elif choice == '8':
            break
        else:
            print("Неверный ввод. Попробуйте снова.")
