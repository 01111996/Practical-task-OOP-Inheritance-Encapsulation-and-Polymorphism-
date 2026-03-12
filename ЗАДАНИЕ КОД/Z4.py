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

def avg_hw_grade(students, course):
    all_grades = []
    for student in students:
        if course in student.grades:
            all_grades.extend(student.grades[course])
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0

def avg_lecture_grade(lecturers, course):
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            all_grades.extend(lecturer.grades[course])
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0


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
    print(student.rate_lecturer(lecturer, 'Python', 7))
    print(student.rate_lecturer(lecturer, 'Java', 8))
    print(student.rate_lecturer(lecturer, 'С++', 8))
    print(student.rate_lecturer(reviewer, 'Python', 6))
    print(lecturer.grades)
    s1 = Student('Анна', 'Смирнова', 'female')
    s1.courses_in_progress += ['Python', 'Git']
    s1.finished_courses += ['Введение в программирование']
    s2 = Student('Борис', 'Кузнецов', 'male')
    s2.courses_in_progress += ['Python', 'Java']
    s2.finished_courses += ['Основы алгоритмов']
    l1 = Lecturer('Елена', 'Волкова')
    l1.courses_attached += ['Python', 'Git']
    l2 = Lecturer('Дмитрий', 'Орлов')
    l2.courses_attached += ['Python', 'Java']
    r1 = Reviewer('Сергей', 'Новиков')
    r1.courses_attached += ['Python', 'Git']
    r2 = Reviewer('Мария', 'Козлова')
    r2.courses_attached += ['Python', 'Java']
    r1.rate_hw(s1, 'Python', 9)
    r1.rate_hw(s1, 'Python', 10)
    r1.rate_hw(s1, 'Git', 8)
    r1.rate_hw(s2, 'Python', 6)
    r2.rate_hw(s2, 'Python', 7)
    r2.rate_hw(s2, 'Java', 9)
    s1.rate_lecturer(l1, 'Python', 10)
    s1.rate_lecturer(l1, 'Git', 9)
    s1.rate_lecturer(l2, 'Python', 8)
    s2.rate_lecturer(l2, 'Python', 7)
    s2.rate_lecturer(l2, 'Java', 10)
    s2.rate_lecturer(l1, 'Python', 9)
    s1.rate_lecturer(l2, 'Git', 5)
    s2.rate_lecturer(r1, 'Python', 8)
    print("=== Студенты ===")
    print(s1)
    print()
    print(s2)
    print()
    print("=== Лекторы ===")
    print(l1)
    print()
    print(l2)
    print()
    print("=== Проверяющие ===")
    print(r1)
    print()
    print(r2)
    print()
    print("=== Сравнение студентов ===")
    print(f's1 > s2: {s1 > s2}')
    print(f's1 < s2: {s1 < s2}')
    print(f's1 == s2: {s1 == s2}')
    print()
    print("=== Сравнение лекторов ===")
    print(f'l1 > l2: {l1 > l2}')
    print(f'l1 < l2: {l1 < l2}')
    print(f'l1 == l2: {l1 == l2}')
    print()
    students = [s1, s2]
    lecturers = [l1, l2]
    print("=== Средние оценки по курсу Python ===")
    print(f'Средняя оценка за д/з (Python): {avg_hw_grade(students, "Python")}')
    print(f'Средняя оценка за лекции (Python): {avg_lecture_grade(lecturers, "Python")}')
    print()
    print("=== Средние оценки по курсу Git ===")
    print(f'Средняя оценка за д/з (Git): {avg_hw_grade(students, "Git")}')
    print(f'Средняя оценка за лекции (Git): {avg_lecture_grade(lecturers, "Git")}')
    print()
    print("=== Средние оценки по курсу Java ===")
    print(f'Средняя оценка за д/з (Java): {avg_hw_grade(students, "Java")}')
    print(f'Средняя оценка за лекции (Java): {avg_lecture_grade(lecturers, "Java")}')