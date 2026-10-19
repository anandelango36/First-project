def greet(name):
    return f"Hello, {name}! Welcome to Python."


def average(marks):
    return sum(marks) / len(marks)


name = input("Enter your name: ")
print(greet(name))

marks = []
for subject in ["Maths", "Science", "English"]:
    score = float(input(f"Enter your {subject} mark: "))
    marks.append(score)

print("Your marks:", marks)
print("Average mark:", round(average(marks), 2))

if average(marks) >= 50:
    print("Result: Pass")
else:
    print("Result: Fail")