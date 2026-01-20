import random
import numpy as np

c_hours, c_teachers, c_days = 7, 11, 5

teachers = [f"nauczyciel_{i}" for i in range(1, c_teachers + 1)]
classes = ["1a", "1b", "1c", "2a", "2b", "3a", "3b", "3c"]
hours = [i for i in range(1, c_hours + 1)]
days = [i for i in range(1, c_days + 1)]
days_names = ["po", "wt", "sr", "cz", "pt"]

### rozklad przedmiot i ich ilosci dla kazdej klasy
subject_limits_1 = {
    "polski": 3,
    "matematyka": 3,
    "angielski": 3,
    "historia": 2,
    "wos": 1,
    "biologia": 1,
    "geografia": 1,
    "chemia": 1,
    "fizyka": 1,
    "informatyka": 1,
    "wf": 3,
    "edb": 1
}

subject_limits_2 = {
    "polski": 3,
    "matematyka": 3,
    "angielski": 3,
    "historia": 1,
    "biologia": 1,
    "geografia": 1,
    "chemia": 1,
    "fizyka": 1,
    "informatyka": 1,
    "wf": 3,
    "podstawy_przedsiebiorczosci": 1
}

subject_limits_3 = {
    "polski": 4,
    "matematyka": 4,
    "angielski": 3,
    "historia": 1,
    "biologia": 1,
    "geografia": 1,
    "chemia": 1,
    "fizyka": 1,
    "wf": 3
}

teacher_subject = {
    "nauczyciel_1": ["matematyka", "fizyka"],
    "nauczyciel_2": ["matematyka", "chemia"],
    "nauczyciel_3": ["polski", "wos", "historia"],
    "nauczyciel_4": ["polski", "angielski"],
    "nauczyciel_5": ["angielski", "polski"],
    "nauczyciel_6": ["historia", "polski"],
    "nauczyciel_7": ["biologia", "wf"],
    "nauczyciel_8": ["matematyka", "geografia", "informatyka"],
    "nauczyciel_9": ["biologia", "edb", "podstawy_przedsiebiorczosci"],
    "nauczyciel_10": ["matematyka", "geografia"],
    "nauczyciel_11": ["angielski", "wf"],
}

### informacje jaki nauczyciel uczy jakich przedmiotow
subject_teacher = {}
for k, v in teacher_subject.items():
    for s in v:
        if s in subject_teacher:
            subject_teacher[s].append(k)
        else:
            subject_teacher[s] = [k]

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
        tabPerClass = np.full((c_hours+1, c_days+1), "-", dtype=object)
        tabPerClass[0, 1:] = days_names
        tabPerClass[1:, 0] = np.arange(1, 8)
    else:
        tabPerClass = np.full((c_hours, c_days), "-", dtype=object)


    print("\tKlasa:", classToW)
    for lesson in table:
        tabPerClass[int(lesson['hour'])-1+legend][int(lesson['day'])-1+legend] = lesson['subject']

    print(tabPerClass)

# TESTS
initial_timetable = generate_random_timetable()
# write_timetable(initial_timetable)
write_timetable_per_class(initial_timetable,"1a",0)

###
