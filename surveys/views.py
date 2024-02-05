import sqlite3

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from surveys.forms import AnswerForm
from surveys.models import Survey, UserAnswer, UserSurvey


def index(request):
    surveys = Survey.objects.all()
    return render(request, 'surveys/index.html', {'surveys': surveys})


@login_required
def survey(request, pk):
    survey = Survey.objects.get(pk=pk)
    if request.method == 'POST':
        user_survey, _ = UserSurvey.objects.get_or_create(
            user=request.user,
            survey=survey,
        )
        last_answer = user_survey.last_answer
        if last_answer and not last_answer.next_question:
            return redirect('surveys:survey_results', pk)
        form = AnswerForm(request.POST or None)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            UserAnswer.objects.create(
                user=request.user,
                answer=answer,
                question=answer.question,
            )
            user_survey.last_answer = answer
            user_survey.save()
            if answer.next_question:
                question = answer.next_question
                form = AnswerForm(answers=question.answers.all())
            else:
                return redirect('surveys:survey_results', pk)
        else:
            if last_answer:
                question = last_answer.next_question
                form = AnswerForm(answers=question.answers.all())
            else:
                question = survey.first_question
                form = AnswerForm(answers=question.answers.all())
        context = {
            'question': question,
            'survey': survey,
            'form': form,
        }
        return render(request, 'surveys/survey.html', context)
    is_started = UserSurvey.objects.filter(
        user=request.user,
        survey=survey,
    ).exists()
    context = {
        'survey': survey,
        'is_started': is_started,
    }
    return render(request, 'surveys/survey.html', context)


@login_required
def survey_results(request, pk):
    # Проверяем, что опрос завершен
    try:
        user_survey = UserSurvey.objects.get(
            user=request.user,
            survey__pk=pk,
        )
    except UserSurvey.DoesNotExist:
        return redirect('surveys:survey', pk=pk)
    if (user_survey.last_answer is None
            or user_survey.last_answer.next_question):
        return redirect('surveys:survey', pk=pk)

    survey = Survey.objects.get(pk=pk)
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    # Общее количество участников опроса
    cursor.execute("""
        SELECT COUNT(*) FROM surveys_usersurvey
        WHERE surveys_usersurvey.survey_id = ?;
    """, (pk,))
    respondents_count = cursor.fetchone()[0]

    # На каждый вопрос
    # Количество ответивших и их доля от общего количества участников опроса
    cursor.execute("""
        SELECT id, text FROM surveys_question WHERE survey_id = ?;
    """, (pk,))
    questions = []
    for row in cursor.fetchall():
        questions.append({
            'id': row[0],
            'text': row[1],
        })
    cursor.execute("""
        SELECT question_id, answer_id
        FROM surveys_useranswer WHERE question_id IN ({});
    """.format(', '.join([str(row['id']) for row in questions])))
    users_answers = []
    for row in cursor.fetchall():
        users_answers.append({
            'question_id': row[0],
            'answer_id': row[1],
        })
    questions_answers = {}
    for answer in users_answers:
        if answer['question_id'] not in questions_answers:
            questions_answers[answer['question_id']] = 1
        else:
            questions_answers[answer['question_id']] += 1
    question_index_number = questions_answers.copy()
    for answer in questions_answers:
        questions_answers[answer] = (
            f'{questions_answers[answer]} / '
            + f'{round(questions_answers[answer] * 100/ respondents_count)} %')
    for question in questions:
        try:
            question['answers_count'] = questions_answers[question['id']]
        except KeyError:
            question['answers_count'] = 0

    # Порядковый номер вопроса по количеству ответивших
    counters = []
    for _, counter in question_index_number.items():
        counters.append(counter)
    counters = sorted(list(set(counters)), reverse=True)
    for id, counter in question_index_number.items():
        question_index_number[id] = counters.index(counter) + 1
    for question in questions:
        try:
            question['index_number'] = question_index_number[question['id']]
        except KeyError:
            question['index_number'] = 999

    # Количество во ответивших на каждый из вариантов ответа
    # и их доля от общего количетва ответивших
    cursor.execute("""
        SELECT id, question_id, text
        FROM surveys_answer WHERE question_id IN ({});
    """.format(', '.join([str(row['id']) for row in questions])))
    answers = {}
    for row in cursor.fetchall():
        if row[1] not in answers:
            answers[row[1]] = [{
                'id': row[0],
                'text': row[2],
                'counter': 0
            }]
        else:
            answers[row[1]].append({
                'id': row[0],
                'text': row[2],
                'counter': 0
            })
    for user_answer in users_answers:
        for answer in answers[user_answer['question_id']]:
            if user_answer['answer_id'] == answer['id']:
                answer['counter'] += 1
    for values in answers.values():
        answers_counter = sum([answer['counter'] for answer in values])
        if answers_counter != 0:
            for answer in values:
                answer['counter'] = (
                    f'{answer["counter"]} / '
                    + f'{round(answer["counter"] * 100 / answers_counter)} %')
    for question in questions:
        question['answers'] = answers[question['id']]

    questions.sort(key=lambda x: (x['index_number'], x['text']))
    connection.close()
    context = {
        'survey': survey,
        'respondents_count': respondents_count,
        'questions': questions,
    }
    return render(request, 'surveys/results.html', context)
