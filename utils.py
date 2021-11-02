my_post = [
    {'id': 1, 'title': "Title 1", 'content': "Content 1"},
    {'id': 2, 'title': "Title 2", 'content': "Content 2"},
]


def find_post(index: int):
    for p in my_post:
        if p['id'] == index:
            return p
    return


def find_index_post(index: int):
    for i, p in enumerate(my_post):
        if p['id'] == index:
            return i
    return
