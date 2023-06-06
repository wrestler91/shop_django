from django.shortcuts import render, redirect

# Create your views here.
def favorites_list(request):
    
    favorites = request.session.get('favorites', [])
    context = {
        'favorites': favorites
    }
    return render(request, 'favorites/favorites_list.html', context=context)

def add_to_favorites(request, id):
    '''
    Добавляет товар в избранное. 
    Вносим в сессию коллекцию favorites в которую заносим информацию о товаре,
    конкретно здесь только id товара
    '''
    if request.method == 'POST':
        # если добавленных товаров нет, то создаем коллекцию в сессии
        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
        # если же товары уже добавлялись, то создаем список с уже добавленными товарами
            request.session['favorites'] = list(request.session['favorites'])
    # print('from add:', request.session['favorites'])
    # использование обычного списка айдишников вместо словаря
    # favorite_id_list = list()
    # for item in request.session['favorites']:
    #     favorite_id_list.append(item)

    # проверка добавлен ли товар уже в избранное, если HE добавлен то возвращает False
    item_exist = next((item for item in request.session['favorites'] if item['id'] == id), False)


    add_data = {
        'id': id,
    }

    # если товар еще не был добавлен, то добавлям данные о товаре в сессию
    # if id not in favorite_id_list:
    if not item_exist:
        request.session['favorites'].append(add_data)
        request.session.modified = True

    return redirect(request.POST.get('url_from'))


def remove_from_favorites(request, id):
    # удаляем элемент из списка избранное
    if request.method == 'POST':
        for item in request.session['favorites']:
            if item['id'] == id:
                item.clear()

    # очищаемизбранное от пустых эллементов
    while {} in request.session['favorites']:
        request.session['favorites'].remove({})
        request.session.modified = True
    # print('from remove:', request.session['favorites'])
    # если список избранного пустой, то удаляем список
    if not request.session['favorites']:
        del request.session['favorites']
        request.session.modified = True

    return redirect(request.POST.get('url_from'))


def delete_favorites(request):
    if request.session.get('favorites'):
        del request.session['favorites']
        request.session.modified = True
    return redirect(request.POST.get('url_from'))
