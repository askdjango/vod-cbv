from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    model = Post

    def head(self, *args, **kwargs):
        try:
            post = self.get_queryset().latest('id')
        except Post.DoesNotExist:
            raise Http404

        response = HttpResponse()
        response['Last-Modified'] = post.updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

post_list = PostListView.as_view()


def greeting_view(message):
    def view_fn(request):
        return HttpResponse(message)
    return view_fn

greeting = greeting_view('Good Day')

morning_greeting = greeting_view('Morning to ya')

evening_greeting = greeting_view('Evening to ya')



@method_decorator(login_required, name='dispatch')
class EditFormView(View):
    model = None
    form_class = None
    success_url = None
    template_name = None

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(self.model, id=pk)

    def get_success_url(self):
        return self.success_url

    def get_template_name(self):
        return self.template_name

    def get_form(self):
        form_kwargs = {
            'instance': self.get_object(),
        }
        if self.request.method == 'POST':
            form_kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return self.form_class(**form_kwargs)

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return kwargs

    def get(self, *args, **kwargs):
        return render(self.request, self.get_template_name(), self.get_context_data())

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        return render(self.request, self.get_template_name(), self.get_context_data(form=form))


post_edit = EditFormView.as_view(
    model=Post,
    form_class=PostForm,
    success_url='/',
    template_name='blog/post_form.html')

