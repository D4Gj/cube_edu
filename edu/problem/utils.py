from .models import Problem, Submission
import requests
import json


def check_submission(code, submission, problem):
    input_test = json.loads(problem.problem_tests_input)
    data = {
        "lang": "python",
        "source": code,
        "tests":
            [{"stdin": value, "mem": problem.memory_limit, "time": problem.time_limit} for value in
             input_test.values()]
    }
    jdata = json.dumps(data)
    response = requests.request("POST", "http://localhost:42920/run", data=jdata,
                                headers={"Accept": "application/json", 'Content-Type': 'application/json'})
    camisole_data = response.json()
    print(camisole_data)
    right_answers = list(json.loads(problem.problem_tests_output).values())
    if camisole_data['success']:
        check_tests = camisole_data['tests']
        for i in range(len(check_tests)):
            if check_tests[i]['exitcode'] == 0:
                if right_answers[i] == check_tests[i]['stdout']:
                    pass
                else:
                    submission.result = 1
                    submission.description = f"Wrong answer {i + 1}"
                    submission.save()
                    return 1
            elif check_tests[i]['exitcode'] == 1:
                submission.result = 2
                submission.description = check_tests[i]['meta']['status']
                submission.save()
                return 2

    submission.result = 0
    submission.description = 'OK'
    submission.save()
    return 0
