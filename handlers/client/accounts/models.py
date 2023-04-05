from db.client.accounts.accounts_db_manager import AccountDB


class Manager:
    def __init__(self):
        self.db_manager = AccountDB()

    def all(self):
        return self.db_manager.all_users()


class User:
    objects = Manager()

    def __init__(self, user_id, superuser=0):
        self.user_id = user_id
        self.superuser = superuser
        self.db_manager = AccountDB()

    def __str__(self):
        return f'User instance with id={self.user_id}'

    def _save(self, su):
        if self.db_manager.check_if_user_in_db(self.user_id):
            return
        self.db_manager.add_user_to_db(user_id=self.user_id, superuser=su)

    def make_admin(self):
        self.db_manager.update_data(table_name='user', id=self.user_id, superuser=1)

    def save_user(self):
        self._save(su=self.superuser)

    def is_superuser(self):
        return self.db_manager.is_superuser(self.user_id)

    def is_creator(self):
        return self.db_manager.is_creator(self.user_id)
