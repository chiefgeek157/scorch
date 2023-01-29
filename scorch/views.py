from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.template import loader

from scorch.models import Scorecard

def index(request):
    return HttpResponse('Index page')

@login_required
def scorecards(request):
    scorecards = Scorecard.objects.order_by('name')
    context = {
        'scorecards': scorecards,
    }
    return render(request, 'scorch/scorecards.html', context)

@login_required
def scorecard_detail(request, scorecard_id):
    scorecard = get_object_or_404(Scorecard, pk=scorecard_id)
    return render(request, 'scorch/scorecard_detail.html',
        {'scorecard': scorecard})
