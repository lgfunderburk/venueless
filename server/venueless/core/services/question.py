from channels.db import database_sync_to_async
from django.db.models import Q

from venueless.core.models.question import Question, QuestionVote


@database_sync_to_async
def create_question(**kwargs):
    new = Question.objects.create(**kwargs)
    return new.serialize_public()


@database_sync_to_async
def get_question(pk, room):
    question = Question.objects.with_score().get(pk=pk, room=room)
    return question.serialize_public()


@database_sync_to_async
def get_questions(room, add_by_user=None, **kwargs):
    questions = Question.objects.filter(room=room)
    if add_by_user:
        questions = questions.filter(Q(**kwargs) | Q(sender=add_by_user))
    elif kwargs:
        questions = questions.filter(**kwargs)
    return [question.serialize_public() for question in questions]


@database_sync_to_async
def update_question(**kwargs):
    question = Question.objects.get(pk=kwargs["id"], room=kwargs["room"])
    for key, value in kwargs.items():
        setattr(question, key, value)
    question.save()
    return question.serialize_public()


@database_sync_to_async
def vote_on_question(pk, room, user, vote):
    if vote is True:  # upvote
        QuestionVote.objects.update_or_create(question_id=pk, sender_id=user.id)
    else:
        QuestionVote.objects.filter(question_id=pk, sender_id=user.id).delete()

    question = Question.objects.with_score().get(pk=pk, room=room)
    return question.serialize_public()
