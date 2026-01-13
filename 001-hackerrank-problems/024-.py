import pandas as pd

students = pd.DataFrame([
    [1, "Alice"],
    [2, "Bob"],
    [13, "John"],
    [6, "Alex"]
], columns=["student_id", "student_name"])

#print(students)

subjects = pd.DataFrame([
    ["Math"],
    ["Physics"],
    ["Programming"]
], columns=["subject_name"])

#print(subjects)

examinations = pd.DataFrame([
    [1, "Math"],
    [1, "Physics"],
    [1, "Programming"],
    [2, "Programming"],
    [1, "Physics"],
    [1, "Math"],
    [13, "Math"],
    [13, "Programming"],
    [13, "Physics"],
    [2, "Math"],
    [1, "Math"]
], columns=["student_id", "subject_name"])

#print(examinations)


stud_exam = students.merge(examinations, on="student_id",how="inner")
stud_exam = stud_exam.groupby(["student_id", "student_name","subject_name"]).agg(attended_exams=('subject_name', 'count')).reset_index()
print(stud_exam)
all_combinations  = students.assign(key=1).merge(subjects.assign(key=1), on='key')
all_combinations = all_combinations.drop(columns=["key"])
print(all_combinations)

stud_exam_1 = all_combinations.merge(stud_exam, on=["student_id", "student_name", "subject_name"],how="left")
stud_exam_1['attended_exams'] = stud_exam_1.attended_exams.astype('Int64').fillna(0)
stud_exam_1 = stud_exam_1.sort_values(by=['student_id','subject_name'], ascending=True).reset_index(drop=True)
print(stud_exam_1)



#print(stud_exam)