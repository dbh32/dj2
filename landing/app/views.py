from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
o = 'original'
t = 'test'
counter_show = Counter({o: 0, t: 0})
counter_click = Counter({o: 0, t: 0})


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    lan_type = request.GET.get('from-landing')
    if lan_type:
        if lan_type == o:
            counter_click[o] += 1
            return render_to_response('index.html')
        elif lan_type == t:
            counter_click[t] += 1
            return render_to_response('index.html')
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    lan_type = request.GET.get('ab-test-arg')
    if lan_type:
        if lan_type == o:
            counter_show[o] += 1
            return render_to_response('landing.html')
        elif lan_type == t:
            counter_show[t] += 1
            return render_to_response('landing_alternate.html')
    return render_to_response('landing.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    try:
        tc = counter_click[t] / counter_show[t]
    except ZeroDivisionError:
        tc = 0

    try:
        oc = counter_click[o] / counter_show[o]
    except ZeroDivisionError:
        oc = 0

    return render_to_response('stats.html', context={
        'test_conversion': round(tc, 2),
        'original_conversion': round(oc, 2),
    })
