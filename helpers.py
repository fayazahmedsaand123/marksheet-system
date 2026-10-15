def calculate_total(english,mathematics,computer,physics,chemistry):
    return english + mathematics + computer + physics + chemistry

def calculate_percentage(total):
    return round((total / 500) * 100,2)

def calculate_result(english,mathematics,computer,physics,chemistry):
    marks = [english,mathematics,computer,physics,chemistry]
    if any(mark < 40 for mark in marks):
        return "Fail"
    return "Pass"

def calculate_grade(percentage,result):
    if result == "Fail":
        return "F"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "E"