from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
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
    colors = "yellow"
    attempts = 0

    def post(self, request, **kwargs):
        self.tried.append(list(request.POST.get("word_guess")))
        self.attempts = len(self.tried)
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attempts"] = self.attempts
        context["tried"] = self.tried
        context["colors"] = self.colors
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
