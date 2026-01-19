from collections import defaultdict

classes = [f"klasa_{i}" for i in range(1, 7)]

teachers = [f"nauczyciel_{i}" for i in range(1, 9)]

subjects = [
    "matematyka",
    "polski",
    "angielski",
    "historia",
    "biologia",
    "geografia"
]

rooms = [f"sala_{i}" for i in range(1, 7)]

days = ["pon", "wt", "sr", "czw", "pt"]
hours = [1, 2, 3, 4, 5, 6]

teacher_subject = {
    "nauczyciel_1": "matematyka",
    "nauczyciel_2": "matematyka",
    "nauczyciel_3": "polski",
    "nauczyciel_4": "polski",
    "nauczyciel_5": "angielski",
    "nauczyciel_6": "historia",
    "nauczyciel_7": "biologia",
    "nauczyciel_8": "geografia"
}

subject_teachers = defaultdict(list)
for teacher, subject in teacher_subject.items():
    subject_teachers[subject].append(teacher)

subject_limits = {
    "matematyka": 3,
    "polski": 3,
    "angielski": 2,
    "historia": 1,
    "biologia": 1,
    "geografia": 1
}

total_required = sum(subject_limits.values())  # 11
