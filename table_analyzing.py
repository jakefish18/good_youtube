import csv
import json

answer_to_int = {
    'не провожу': 0,
    'до 30 минут': 0.5,
    'до 1 часа': 1,
    'до 2 часов': 2,
    'до 3 часов': 3,
    'до 4 часов': 4,
    'до 5 часов': 5,
    'больше 5 часов': 5.5
}

time_answers = {
    'не провожу': 0,
    'до 30 минут': 0,
    'до 1 часа': 0,
    'до 2 часов': 0,
    'до 3 часов': 0,
    'до 4 часов': 0,
    'до 5 часов': 0,
    'больше 5 часов': 0
} 

answers_statistic = {
    'До 14 лет': {
        'youtube': time_answers.copy(),
        'tik_tok': time_answers.copy()
    },
    'С 14 лет до 18 лет': {
        'youtube': time_answers.copy(),
        'tik_tok': time_answers.copy()
    },
    'С 18 лет до 25 лет': {
        'youtube': time_answers.copy(),
        'tik_tok': time_answers.copy()
    },
    'С 25 лет до 38 лет': {
        'youtube': time_answers.copy(),
        'tik_tok': time_answers.copy()
    },
    'Больше 38 лет': {
        'youtube': time_answers.copy(),
        'tik_tok': time_answers.copy()
    }
}

with open('Новая форма (Ответы) - Ответы на форму (1).csv', 'r', encoding='utf-8') as file:
    file_reader = csv.reader(file, delimiter = ",")

    for row in file_reader:
        date, time_youtube, time_tik_tok, age = row

        answers_statistic[age]['youtube'][time_youtube] += 1
        answers_statistic[age]['tik_tok'][time_tik_tok] += 1


    for age in answers_statistic:
        print(age)
        for platform in answers_statistic[age]:
            print(f'\t{platform}')
            all_answer_sum = 0
            interviewees = 0

            for answer_type, answer_num in answers_statistic[age][platform].items():
                print(f'\t\t{answer_type} ответов у {answer_num} участников')

                all_answer_sum += answer_to_int[answer_type] * int(answer_num)
                interviewees += int(answer_num)
            
            print(f'\t\t{all_answer_sum / interviewees}')