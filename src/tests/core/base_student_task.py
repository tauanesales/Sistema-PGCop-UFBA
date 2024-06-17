from datetime import datetime

from core import base_student

task_id = 1

name = "Title for the Task 1"
description = "The goal is helping 70% of people around the world about how to Avast!"
completed = 0
deadline_date = str(datetime.now().date())

last_notified = None
completion_date = None

alternative_name = "Another Title for the Task 2"
alternative_description = "The goal of this task is getting gold 4 at the new CS:GO 2"


student_form = {
    "nome": base_student.name,
    "cpf": base_student.cpf,
    "email": base_student.email,
    "matricula": base_student.registration,
    "curso": base_student.course,
    "senha": base_student.password,
    "telefone": base_student.phone,
    "lattes": base_student.lattes,
    "data_ingresso": base_student.admission_date,
    "data_defesa": base_student.defense_date,
    "data_qualificacao": base_student.qualification_date,
    "orientador_id": base_student.advisor_id,
}
