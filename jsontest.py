import json
import re
from password_strength import PasswordPolicy, PasswordStats

"""with open('final_questions.json') as q_file:
    questions = json.loads(q_file.read())
with open('final_questions.json','w') as q_file:
    q_file.write(json.dumps(questions,indent=4))"""
policy = PasswordPolicy.from_names(
    length=8,
    strength=0.2,
    uppercase=1,
    numbers=1
)
if __name__ == '__main__':
    current_password = policy.password('J1/A#077')
    print(current_password.strength())
    violations = current_password.test()
    if len(violations) == 0:
        print("The password has passed the test!")
    elif str(violations[0]).startswith('Length'):
        print("The length of the password should be at least 8 ! ")
    elif str(violations[0]).startswith('Strength'):
        print("The password is too weak!")

