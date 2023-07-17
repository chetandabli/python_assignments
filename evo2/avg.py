company = {
    'employees': {
        'John': {'age': 35, 'job_title': 'Manager'},
        'Emma': {'age': 28, 'job_title': 'Software Engineer'},
        'Kelly': {'age': 41, 'job_title': 'Senior Developer'},
        'Sam': {'age': 30, 'job_title': 'Software Engineer'},
        'Mark': {'age': 37, 'job_title': 'Senior Manager'},
        'Sara': {'age': 32, 'job_title': 'Software Engineer'},
    }
}

def average_age_of_employees_with_s_job_title(company):
    count = 0
    total = 0

    for employees in company["employees"]:
        if company["employees"][employees]['job_title'][0] == "S":
            count += 1
            total += company["employees"][employees]["age"]

    if count == 0:
        return 0
    else:
        return total/count

print(average_age_of_employees_with_s_job_title(company))
