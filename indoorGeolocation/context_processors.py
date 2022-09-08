def names(request):
    names = ["Chambre" + str(i) for i in range(5, 11)]
    return {'names': names, 'request': request}
