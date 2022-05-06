from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post
from .forms import NewsForm
from .filters import NewsFilter


class NewsList(ListView):
    model = Post
    ordering = ["-creation_time"]
    template_name = "news_list.html"
    context_object_name = "news_list"
    paginate_by = 5


class NewsDetail(DetailView):
    model = Post
    template_name = "news_detail.html"
    context_object_name = "news_detail"


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'

    template_name = "news_add.html"
    form_class = NewsForm
    success_url = '/news/'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'

    template_name = 'news_add.html'
    form_class = NewsForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        _id = self.kwargs.get('pk')
        return Post.objects.get(pk=_id)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'

    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class NewsSearch(ListView):
    model = Post
    ordering = ['-creation_time']
    context_object_name = "news_list"
    template_name = 'news_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context
