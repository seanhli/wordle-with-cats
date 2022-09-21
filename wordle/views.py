from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from wordle.word_generator import word_generator
from wordle.models import WordleHistory

# Create your views here.
class WordleHistoryList(ListView):
    model = WordleHistory
    template_name = "wordle/history.html"

    def get_queryset(self):
        return WordleHistory.objects.order_by("-attempted_at").filter(player=self.request.user)

class GameBoard(DetailView):
    model = WordleHistory
    template_name = "wordle/board.html"
    tried = []
    attempts = 0
    error_message = ""
    current_board = []

    def post(self, request, **kwargs):
        user_guess = request.POST.get("word_guess").upper()
        self.object = self.get_object()
        gen = word_generator()

        print("diagnose: ", self.attempts, self.current_board, self.object.id)

        if not self.current_board:
            self.tried.clear()
        elif self.current_board[0] != self.object.id:
            self.tried.clear()
            self.current_board.clear()

        if len(user_guess) != self.object.length:
            self.error_message = "Invalid length. Please try again"
        elif not gen.check_word(user_guess):
            self.error_message = "Invalid word. Please try again"
        else:
            self.tried.append(gen.check_answer(user_guess,self.object.word.upper()))
        self.attempts = len(self.tried)

        if not self.current_board:
            self.current_board.append(self.object.id)

        if user_guess == self.object.word.upper():
            self.object.cleared = True
            self.object.guesses_needed = self.attempts
            self.object.save()

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context["attempts"] = self.attempts

        if self.attempts == 0:
            self.tried.clear()

        board = self.tried.copy()
        for i in range(self.attempts,self.object.tries,1):
            board.append([])
            for k in range(self.object.length):
                board[i].append("")
        context["tried"] = board

        context["error_message"] = self.error_message
        print(context)
        return context


class WordleCreateView(CreateView):
    model = WordleHistory
    template_name = "wordle/newgame.html"
    fields = ["length","tries","duplicates"]

    def form_valid(self, form):
        form.instance.player = self.request.user
        form.instance.guesses_needed = 0

        cl = (form.instance.length**0.5)*25
        if form.instance.duplicates:
            cl += 15
        cl += (6-(form.instance.tries-(form.instance.length-5)))*10

        score = ""
        match cl:
            case _ if cl < 30:
                score = "Very easy"
            case _ if cl < 50:
                score = "Easy"
            case _ if cl < 70:
                score = "Moderate"
            case _ if cl < 100:
                score = "Difficult"
            case _ if cl >= 100:
                score = "Very difficult"

        form.instance.difficulty = score
        gen = word_generator()
        form.instance.word = gen.generate_random_word(form.instance.length, not form.instance.duplicates)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("game_board", kwargs={"pk": self.object.id})
