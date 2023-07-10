def max_salary_employee(employees):
    high = 0
    highobj = {"name": None, "salary": None, "designation": None}

    for employee in employees:
        if employee["salary"] > high:
            highobj["name"] = employee["name"]
            highobj["salary"] = employee["salary"]
            highobj["designation"] = employee["designation"]
            high = employee["salary"]
    
    print(highobj)

employee = [
    {"name": "John", "salary": 2000, "designation": "developer"},
    {"name": "Chetan", "salary": 5000, "designation": "CEO"},
    {"name": "Gyan", "salary": 2500, "designation": "HR"}
]

max_salary_employee(employee)