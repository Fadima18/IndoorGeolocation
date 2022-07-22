def names(request):
    # names = ['tidiane', 'aziz', 'fasou', 'assane', 'fallou', 'ass', 'mor', 'youssou', 'empty', 'bachir', 'mounir', 'moustapha']
    names = ["Chambre" + str(i) for i in range(5, 11)]
    return {'names': names}