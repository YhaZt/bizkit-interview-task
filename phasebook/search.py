from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """
    id = args.get('id')
    name = args.get('name')
    age = args.get('age')
    occupation = args.get('occupation')

    results = []
    sorted_results = []

    def add_user(user, matched_on):
        if user not in results:
            results.append((user, matched_on))

    if id:
        for user in USERS:
            if user['id'] == id:
                add_user(user, 'id')

    if name:
        name = name.lower()
        for user in USERS:
            if name in user['name'].lower():
                add_user(user, 'name')

    if age:
        age = int(age)
        for user in USERS:
            if age - 1 <= user['age'] <= age + 1:
                add_user(user, 'age')

    if occupation:
        occupation = occupation.lower()
        for user in USERS:
            if occupation in user['occupation'].lower():
                add_user(user, 'occupation')

    if not args:
        return USERS
    priority_order = {'id': 1, 'name': 2, 'age': 3, 'occupation': 4}
    results.sort(key=lambda x: priority_order[x[1]])
    sorted_results = [user[0] for user in results]

    return sorted_results
