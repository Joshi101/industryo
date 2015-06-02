from django.db import models
from django.contrib.auth.models import User
from tags.models import Tags
from nodes.models import Images
from industryo.unique_slug import unique_slugify
from activities.models import Activity


class Question(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    question = models.TextField(max_length=5000, null=True, blank=True)
    votes = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)
    time = models.TimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags)
    images = models.ManyToManyField(Images)
    admin_score = models.IntegerField(default=1)
    # score
    # last active


    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ('-time',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.title
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
            super(Question, self).save(*args, **kwargs)

    def get_all_question(self):
        all_question = Question.objects.all()[:50]
        return all_question

    def get_unanswered(self):
        all_unanswered = Question.objects.filter(answered=False)[:20]
        return all_unanswered

    def get_tagged(self, tag):
        all_tagged = Question.objects.filter()

    def create_tags(self, tag):
        # tags = tags.strip()
        tag_list = tag.split(',')
        for ta in tag_list:
            print(ta)
            t, created = Tags.objects.get_or_create(tag=ta)
            # self.tags(tags=t, question=self)

    def get_q_upvoters(self):
        upvotes = Activity.objects.filter(question=self.pk, activity='U')
        list = []
        for upvote in upvotes:
            list.append(upvote.user)
        return list

    def get_q_downvoters(self):
        downvotes = Activity.objects.filter(question=self.pk, activity='D')
        list = []
        for downvote in downvotes:
            list.append(downvote.user)
        return list

    def get_votes(self):
        upvotes = Activity.objects.filter(question=self.pk, activity='U').count()
        downvotes = Activity.objects.filter(question=self.pk, activity='D').count()
        votes = upvotes-downvotes
        self.votes=votes
        self.save()
        return votes

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])
        else:
            return value

    def get_answer_preview(self):
        answer = Answer.objects.filter(question=self.pk)[:1]
        if answer:
            for a in answer:
                ans = a.answer
                return ans

        else:
            return "no answers till now"
        # ans = answer.answer
        # # preview = self.get_summary(ans.answer)
        # return ans






class QuestionComment(models.Model):
    question = models.ForeignKey(Question)
    comment = models.TextField(max_length=500)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Question Comment"
        verbose_name_plural = "Question Comments"
        ordering = ("time",)

    def all_ques_comment(self, qid):
        all_comment = QuestionComment.objects.filter(question=qid)
        return all_comment


class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    votes = models.IntegerField(default=0)
    answer = models.TextField(max_length=10000)
    # count = models.IntegerField()
    time = models.TimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    images = models.ManyToManyField(Images)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ('-is_accepted', '-votes', 'time',)

    def __str__(self):
        return self.answer

    def all_answer(self, qid):
        all_ans = Answer.objects.filter(question=qid)
        return all_ans


class AnswerComment(models.Model):
    answer = models.ForeignKey(Answer)
    comment = models.TextField(max_length=500)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Answer Comment"
        verbose_name_plural = "Answer Comments"
        ordering = ("time",)

    def all_ans_comment(self, aid):
        all_comment = AnswerComment.objects.filter(answer=aid)
        return all_comment





# Create your models here.
