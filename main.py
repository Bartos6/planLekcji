import random
import numpy as np


c_hours, c_teachers, c_days = 7, 30, 5

teachers = [f"nauczyciel_{i}" for i in range(1, c_teachers + 1)]
classes = ["1a", "1b", "1c", "2a", "2b", "3a", "3b", "3c"]
hours = [i for i in range(1, c_hours + 1)]
days = [i for i in range(1, c_days + 1)]

days_names = ["po", "wt", "sr", "cz", "pt"]
subjects_names = {
    1: "polski",
    2: "matematyka",
    3: "angielski",
    4: "wf",
    5: "biologia",
    6: "geografia",
    7: "chemia",
    8: "fizyka",
    9: "informatyka",
    10: "historia",
    11: "edb",
    12: "pp",
    13: "wos"
}


# randomowe przydzielenie przedmiotow nauczycielom. Przedmioty 1-4 (najwiecej godzin) sa przydzielane domyslnie
def generate_random_teacher_subject_Beta():
    teacher_subject = {}

    i = 0
    subjectsTab = [i for i in range(1, len(subjects_names) + 1)]
    for teacher in teachers:
        teacher_subject[teacher] = [i % 4 + 1] + random.sample(range(5, len(subjects_names) + 1), 2)
        i += 1
    return teacher_subject

def generate_subject_teacher(teacher_subject):
    subject_teacher = {}
    for k, v in teacher_subject.items():
        for s in v:
            if s in subject_teacher:
                subject_teacher[s].append(k)
            else:
                subject_teacher[s] = [k]
    return subject_teacher

def generate_teacher_subject_relation():
    teacher_subject = generate_random_teacher_subject_Beta()
    subject_teacher = dict(sorted(generate_subject_teacher(teacher_subject).items()))

    while len(subject_teacher) != len(subjects_names):
        teacher_subject = generate_random_teacher_subject_Beta()
        subject_teacher = dict(sorted(generate_subject_teacher(teacher_subject).items()))
    return teacher_subject, subject_teacher

teacher_subject, subject_teacher = generate_teacher_subject_relation()

### rozklad przedmiot i ich ilosci dla kazdej klasy
subject_limits_1 = {
    1: 3,
    2: 3,
    3: 3,
    4: 3,
    5: 1,
    6: 1,
    7: 1,
    8: 1,
    9: 1,
    10: 1,
    11: 1,
    12: 1
}

subject_limits_2 = {
    1: 3,
    2: 4,
    3: 3,
    4: 3,
    5: 1,
    6: 1,
    7: 1,
    8: 1,
    9: 1,
    10: 1,
    11: 1,

    13: 1
}

subject_limits_3 = {
    1: 4,
    2: 4,
    3: 3,
    4: 3,
    5: 1,
    6: 1,
    7: 1,
    8: 1,

    13: 2
}

###generowanie tablicy z przedmiotami ktore musza zrealizowac klasy 1,2,3
subjects_required_1 = []
for k, v in subject_limits_1.items():
    for _ in range(v):
        subjects_required_1.append(k)

subjects_required_2 = []
for k, v in subject_limits_2.items():
    for _ in range(v):
        subjects_required_2.append(k)

subjects_required_3 = []
for k, v in subject_limits_3.items():
    for _ in range(v):
        subjects_required_3.append(k)

subjects_required = [subjects_required_1, subjects_required_2, subjects_required_3]

### dostepna siatka godzin
day_time = []
for i in range(c_hours * len(days)):
    day_time.append(str(days[i // c_hours]) + str(hours[i % c_hours]))


### generowanie losowego harmonogramu
def generate_random_timetable():
    timetable = []

    # losowa zmiana kolejności przedmiotów
    for sub in subjects_required:
        for i in range(len(sub)):
            swapId = random.randint(0, len(sub) - 1)
            sub[i], sub[swapId] = sub[swapId], sub[i]

    # losowa zmiana kolejności day_time
    for i in range(len(day_time)):
        swapId = random.randint(0, len(day_time) - 1)
        day_time[i], day_time[swapId] = day_time[swapId], day_time[i]

    for class_name in classes:
        grade = int(class_name[0]) - 1
        for i in range(len(subjects_required[grade])):
            subject = subjects_required[grade][i]
            teacher = random.choice(subject_teacher[subject])
            day = day_time[i][0:1]
            hour = day_time[i][1:]

            lesson = {
                'class': class_name,
                'day': day,
                'hour': hour,
                'subject': subject,
                'teacher': teacher
            }
            timetable.append(lesson)
    return timetable


### zlikwidowanie powtarzajacych sie lekcji u teacher

def teacherNoDouble(timetable, licznik=0):
    teacher_schedule = {}
    for lesson in timetable:
        teacher = lesson['teacher']
        class_name = lesson['class']
        day = lesson['day']
        hour = lesson['hour']

        teacher_key = (teacher, day, hour)
        teacher_schedule[teacher_key] = teacher_schedule.get(teacher_key, 0) + 1

    flag = 0
    for key, count in teacher_schedule.items():
        if count > 1:
            flag = 1
            break

    if flag == 1:
        licznik += 1
        return teacherNoDouble(generate_random_timetable(), licznik)
    else:
        print(f"Wykonano po {licznik} wywolaniach funkcji")
        return timetable


### wypisywanie tablicy w formacie tabeli 2-wymairowej
def write_timetable(timetable):
    posortowane = sorted(timetable, key=lambda x: x["hour"])
    posortowane.sort(key=lambda x: x["day"])
    posortowane.sort(key=lambda x: x["class"])

    for i in range(len(posortowane)):
        if i == 0 or posortowane[i]['class'] != posortowane[i - 1]['class']:
            print("klasa:", posortowane[i]['class'])

        print(posortowane[i]['day'], posortowane[i]['hour'], posortowane[i]['subject'])


def write_timetable_per_class(timetable, classToW, legend):
    table = [x for x in timetable if x["class"] == classToW]
    table.sort(key=lambda x: x["hour"])
    table.sort(key=lambda x: x["day"])
    if legend == True:
        tabPerClass = np.full((c_hours + 1, c_days + 1), "-", dtype=object)
        tabPerClass[0, 1:] = days_names
        tabPerClass[1:, 0] = np.arange(1, 8)
    else:
        tabPerClass = np.full((c_hours, c_days), "-", dtype=object)

    print("\tKlasa:", classToW)
    for lesson in table:
        tabPerClass[int(lesson['hour']) - 1 + legend][int(lesson['day']) - 1 + legend] = lesson['subject']

    print(tabPerClass)


###
def fitness_function(timetable):
    score = 0
    # weights of costs
    w_classDoubleLesson = -100
    w_teacherDoubleLesson = -100
    w_classBreakCost = -10
    w_teacherBreakCost = -5
    w_numberOfLessonsPerDayCost = -5

    # Class conflicts: a class have more than one lesson at the same time
    class_schedule = {}
    for lesson in timetable:
        teacher = lesson['teacher']
        class_name = lesson['class']
        day = lesson['day']
        hour = lesson['hour']

        class_key = (class_name, day, hour)
        class_schedule[class_key] = class_schedule.get(class_key, 0) + 1

    classDoubleLesson = 0
    for key, count in class_schedule.items():
        if count > 1:
            classDoubleLesson += (count - 1)

    score = classDoubleLesson * w_classDoubleLesson

    # Teacher conflicts: a teacher teaching more than one class at the same time
    teacher_schedule = {}
    for lesson in timetable:
        teacher = lesson['teacher']
        class_name = lesson['class']
        day = lesson['day']
        hour = lesson['hour']

        teacher_key = (teacher, day, hour)
        teacher_schedule[teacher_key] = teacher_schedule.get(teacher_key, 0) + 1

    teacherDoubleLesson = 0
    for key, count in teacher_schedule.items():
        if count > 1:
            teacherDoubleLesson += (count - 1)

    score = teacherDoubleLesson * w_teacherDoubleLesson
    # Class Warning: The class has as few empty activities as possible in the middle of the day. "-"
    classBreakCost = 0

    for class_name in classes:
        table = [x for x in timetable if x["class"] == class_name]
        table.sort(key=lambda x: x["hour"])
        table.sort(key=lambda x: x["day"])

        for i in range(len(table)):
            if table[i]["day"] != table[i - 1]["day"]:
                continue
            classBreakCost += int(table[i]["hour"]) - int(table[i - 1]["hour"]) - 1

    score += classBreakCost * w_classBreakCost

    # Teacher warning: Teacher should have as few empty lessons as possible in the middle of the day.  teacherBreakCost = 0
    teacherBreakCost = 0
    for teacher in teachers:
        table = [x for x in initial_timetable if x["teacher"] == teacher]
        table.sort(key=lambda x: x["hour"])
        table.sort(key=lambda x: x["day"])

        for i in range(len(table)):
            if table[i]["day"] != table[i - 1]["day"] or i == 0 or int(table[i]["hour"]) - int(
                    table[i - 1]["hour"]) == 0:
                continue
            teacherBreakCost += int(table[i]["hour"]) - int(table[i - 1]["hour"]) - 1

    score += teacherBreakCost * w_teacherBreakCost

    # Class warning: The median number of lessons per day is similar to the average number of lessons per day.
    numberOfLessonsPerDayCost = 0
    classPerDay = {}

    for lesson in initial_timetable:
        classPerDay[(lesson['class'], lesson['day'])] = classPerDay.get((lesson['class'], lesson['day']), 0) + 1

    class_lessonPerDay = {}
    for (class_name, day), number in sorted(classPerDay.items()):
        if class_name not in class_lessonPerDay:
            class_lessonPerDay[class_name] = []
        class_lessonPerDay[class_name].append(number)

    for class_name, tabNumber in class_lessonPerDay.items():
        mean = np.mean(tabNumber)
        median = np.median(tabNumber)
        if mean != median:
            if mean > median:
                numberOfLessonsPerDayCost += mean - median
            else:
                numberOfLessonsPerDayCost += median - mean
    numberOfLessonsPerDayCost *= 100
    score += numberOfLessonsPerDayCost * w_numberOfLessonsPerDayCost

    return score



def crossover(parent1, parent2):
    cut_day = random.randint(1, c_days-1)
    child = []

    for p1, p2 in zip(parent1, parent2):
      if int(p1['day']) <= cut_day:
          child.append(p1)
      else:
          child.append(p2)
    return child


def mutate_teacher(timetable, mutation_rate=0.1):
    mutate_table = [lesson.copy() for lesson in timetable]

    for lesson in mutate_table:
        if random.random() < mutation_rate:
            lesson['teacher'] = random.choice(subject_teacher[lesson["subject"]])

    return mutate_table


def mutate_swap_lessons(timetable, mutation_rate=0.1):
    mutate_table = [lesson.copy() for lesson in initial_timetable]
    startId, endId, temp = 0, 0, 0
    for i in range(len(mutate_table)):
        endId = len(subjects_required[int(mutate_table[i]["class"][0]) - 1]) + temp - 1

        if random.random() < 0.1:
            swapId = random.randint(startId, endId)
            mutate_table[i]["subject"], mutate_table[swapId]["subject"] = mutate_table[swapId]["subject"], \
                                                                          mutate_table[i]["subject"]

        if i == endId:
            startId = endId + 1
            temp += len(subjects_required[int(mutate_table[i]["class"][0]) - 1])

    return mutate_table


# tworzenie table  ##########################################################################
initial_timetable = generate_random_timetable()
initial_timetable2 = generate_random_timetable()


child = crossover(initial_timetable,initial_timetable2)

a = initial_timetable.copy()
b = mutate_swap_lessons(a)



print("score:", fitness_function(child))
