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


class GameBoard(DetailView):
    model = WordleHistory
    template_name = "wordle/board.html"
    tried = []
    attempts = 0
    error_message = ""
    current_board = 0

    def post(self, request, **kwargs):
        user_guess = request.POST.get("word_guess").upper()
        self.object = self.get_object()
        gen = word_generator()

        if self.attempts == 0 or self.current_board != self.object.id:
            self.tried = []

        if len(user_guess) != self.object.length:
            self.error_message = "Invalid length. Please try again"
        elif not gen.check_word(user_guess):
            self.error_message = "Invalid word. Please try again"
        else:
            self.tried.append(gen.check_answer(user_guess,self.object.word.upper()))
        self.attempts = len(self.tried)
        self.current_board = self.object.id
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context["attempts"] = self.attempts

        if self.attempts == 0 or self.current_board != self.object.id:
            self.tried = []

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
        gen = word_generator()
        form.instance.word = gen.generate_random_word(form.instance.length, not form.instance.duplicates)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("game_board", kwargs={"pk": self.object.id})
