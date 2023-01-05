import json
import os.path


def start():
    answer_handle()
    print('perfect!')


def json_handle(path: str):
    if not os.path.exists(path): return {}
    with open(path, mode='r', encoding='utf-8') as f:
        content = f.read()
    if content == "": return {}
    return json.loads(content)


def answer_handle():
    answer_bank = json_handle("./answer.json")
    answer_catalog = ("判断答案", "选择答案", "填空答案", "程序填空答案", "temp_ans")
    for file in answer_catalog:
        temp_answer = json_handle(f"./{file}.json")
        if not temp_answer: continue
        temp_answer = temp_answer['submission']['submissionDetails']
        if not temp_answer: continue
        for answer in temp_answer:
            answer_bank[answer['problemSetProblemId']] = get_answer(answer)
    # answer['trueOrFalseSubmissionDetail']['answer'] or answer[
    #     'fillInTheBlankSubmissionDetail']['answer'] or answer['fillInTheBlankSubmissionDetail']['answer']
    with open("./answer.json", mode='w', encoding='utf-8') as f:
        f.write(json.dumps(answer_bank))
    question_handle(answer_bank)


def get_answer(item: dict):
    for i in item:
        if isinstance(item[i], dict):
            if not item[i].get('answer'):
                return item[i].get('answers')
            else:return item[i].get('answer')


def question_handle(answer_bank):
    question_type = ("判断", "选择", "填空", "程序填空")
    for item in question_type:
        question_list = json_handle(f"./{item}.json")
        if question_list == {} or answer_bank == {}: continue
        for question in question_list["problemSetProblems"]:
            answer = answer_bank.get(question['id'], "#")
            info = get_info(question['title'], answer)
            with open(f"./题库/{item}.txt", mode='a', encoding='utf-8') as f:
                f.write(info)


def get_info(title, answer):
    if isinstance(answer, list):
        temp_ans = ""
        for item in answer:
            temp_ans = temp_ans.__add__(item).__add__(" ")
        return f"{title}答案：{temp_ans}\n"
    return f"{title}答案：{answer}\n"


start()
