class ResponseMessage:
    post = "Created"
    put = "Updated"
    delete = "Deleted"
    no_data = "Invalid input"


my_post = [
    {'id': 1, 'title': "Title 1", 'content': "Content 1"},
    {'id': 2, 'title': "Title 2", 'content': "Content 2"},
]


def find_post(pk: int):
    for p in my_post:
        if p['id'] == pk:
            return p
    return
