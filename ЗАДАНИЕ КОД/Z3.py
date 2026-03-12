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
            print("Ошибка: лектор не закреплён за курсом или студент на него не записан")

    def _average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0
    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {self._average_grade():.1f}\n"
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
        self.grades = {}  # оценки от студентов: {курс: [список оценок]}

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

if __name__ == '__main__':
    student1 = Student('Ruoy', 'Eman', 'male')
    student1.courses_in_progress += ['Python', 'Git']
    student1.finished_courses += ['Введение в программирование']
    student2 = Student('Ivan', 'Ivanov', 'male')
    student2.courses_in_progress += ['Python']

    lecturer1 = Lecturer('Some', 'Buddy')
    lecturer1.courses_attached += ['Python']
    lecturer2 = Lecturer('Another', 'Teacher')
    lecturer2.courses_attached += ['Python']

    reviewer1 = Reviewer('Some', 'Buddy')
    reviewer1.courses_attached += ['Python', 'Git']
    reviewer1.rate_hw(student1, 'Python', 10)
    reviewer1.rate_hw(student1, 'Python', 9)
    reviewer1.rate_hw(student2, 'Python', 7)

    student1.rate_lecturer(lecturer1, 'Python', 10)
    student1.rate_lecturer(lecturer1, 'Python', 9)
    student2.rate_lecturer(lecturer2, 'Python', 8)

    print(student1)
    print()
    print(f'lecturer1 > lecturer2: {lecturer1 > lecturer2}')
    print(f'lecturer1 < lecturer2: {lecturer1 < lecturer2}')
    print(f'lecturer1 == lecturer2: {lecturer1 == lecturer2}')
    print()
    print(f'student1 > student2: {student1 > student2}')
    print(f'student1 < student2: {student1 < student2}')
    print(f'student1 == student2: {student1 == student2}')
    print()

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
