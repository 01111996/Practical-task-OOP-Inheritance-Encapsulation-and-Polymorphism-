class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer)
                and course in self.courses_in_progress
                and course in lecturer.courses_attached
        ):
            if 1 <= grade <= 10:
                if course in lecturer.grades:
                    lecturer.grades[course].append(grade)
                else:
                    lecturer.grades[course] = [grade]
            else:
                print("Оценка должна быть от 1 до 10")
        else:
            print("Ошибка")

    def _average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка: {self._average_grade():.1f}\n"
            f"Курсы в процессе изучения: {', '.join(self.courses_in_progress) or 'нет'}\n"
            f"Завершённые курсы: {', '.join(self.finished_courses) or 'нет'}"
        )
    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() == other._average_grade()

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {self._average_grade():.1f}"
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() == other._average_grade()

class Reviewer(Mentor):

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"

lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

print(student.rate_lecturer(lecturer, 'Python', 7))   # None
print(student.rate_lecturer(lecturer, 'Java', 8))     # Ошибка
print(student.rate_lecturer(lecturer, 'С++', 8))      # Ошибка
print(student.rate_lecturer(reviewer, 'Python', 6))   # Ошибка

print(lecturer.grades)  # {'Python': [7]}