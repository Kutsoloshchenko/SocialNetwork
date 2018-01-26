"""Module that providets post functions like create, edit, like  and delete posts"""

def except_errors(function):
    def wrapper(self, data):
        try:
            return function(self, data)
        except Exception as e:
            return {"result": "failed", "exception": "type: %s, error message: %s" % (str(type(e)), str(e))}

    return wrapper

class PostController:

    def __init__(self, db):
        self._db = db
        self._table_alias = 'post'

    def _create_part_index(self, title, number):

        if number == 2:
            title = title + " part %d" % number
        else:
            title = title.replace(' part %d' % (number - 1), " part %d" % number)

        return title

    @except_errors
    def create_post(self, data, number=2):
        """ Creates post with specified title and content"""


        if self._db.contains(self._table_alias, {"owner":data['owner'].id, "title":data['title']}):

            self._create_part_index(data['title'], number)

            return self.create_post(data, number+1)

        else:
            self._db.add_entry(self._table_alias, data)
            return {"result": "ok", "id": self._db.get_entry(self._table_alias, data)}

    @except_errors
    def get_posts(self, data):

        if 'owner' in data.keys():
            data['owner'] = self._db.get_entry('user', {"id":data['owner']}, asEntry=True)

        return self._db.get_entries(self._table_alias, data)

    @except_errors
    def delete_post(self, data):
        self._db.delete_entry(self._table_alias, data)
        return {"result": "ok"}

    @except_errors
    def edit_post(self, data):
        id = data.pop('id')
        owner = data.pop('owner').id
        original_entry = self._db.get_entry(self._table_alias, {"id":id})

        if original_entry['title'] != data['title']:
            wrong_name = True
            number = 1
            while wrong_name:
                if self._db.contains(self._table_alias, {"owner": owner,"title":data['title']}):
                    data['title'] = self._create_part_index(data['title'], number+1)
                else:
                    wrong_name = False

        self._db.update_entry(self._table_alias, data, {"id":id})

        return {"result": "ok"}

    @except_errors
    def update_like(self, data):
        post = self._db.get_entry(self._table_alias, {'id': data['id']})

        likes = post['likes'].split()

        print(likes)
        print(data['user id'])

        if str(data['user id']) in likes:
            likes.remove(str(data['user id']))
        else:
            likes.append(str(data['user id']))

        self._db.update_entry(self._table_alias, {"likes": ' '.join(id for id in likes)}, {'id': data['id']})

        return {"result": "ok"}
