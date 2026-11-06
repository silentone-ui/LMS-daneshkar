from locust import HttpUser,task,between


class BookApiUser(HttpUser):
    wait_time = between(1,3)


@task
def list_books(self):
    self.client.get('/blog/api/books/')

@task
def viewset_book_list(self):
    self.client.get('/blog/viewset/books/')

@task
def create_book(self):
    payload = {
        'title':'world war II',
        'author' : 1,
    }

    headers = {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkzNjIxMDI2LCJpYXQiOjE3OTM1MzQ2MzAsImp0aSI6IjBiNTYxNzhhMzNhNTQ0ZmNiNjM5ZjAzYzM3MjQxZDc5IiwidXNlcl9pZCI6IjEiLCJmaXJzdF9uYW1lIjoibWFqaWQiLCJsYXN0X25hbWUiOiJzYWRlZ2hpIiwiaXNfc3RhZmYiOnRydWUsInBob25lIjoiMDkxMDA0NDUyODcifQ.AF2PXJZqAysIIJt2wcTHQk3QreezclDjCyYNZl8NzfU",
        'authorization' : ''
    }

    self.client.post('/blog/viewset/books',json=payload,headers=headers)