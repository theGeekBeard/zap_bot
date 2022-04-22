class Database:

    def __init__(self, con):
        self.db = con
        self.sql = self.db.cursor()

    # Setters
    async def add_index(self, chat_id, index):
        with self.db:
            if await self.get_index(chat_id) is not None:
                self.sql.execute(f"UPDATE navigation SET index={index} WHERE chat_id={chat_id}")
            else:
                self.sql.execute(f"INSERT INTO navigation(chat_id, index) VALUES({chat_id}, {index})")

    async def del_index(self, chat_id):
        with self.db:
            self.sql.execute(f"DELETE FROM navigation WHERE chat_id = {chat_id}")

    async def get_index(self, chat_id):
        self.sql.execute(f"SELECT index FROM navigation WHERE chat_id={chat_id}")
        index = self.sql.fetchone()
        print(index)
        if index:
            return index[0]
        else:
            return None

    async def add_message_id(self, chat_id, message_id):
        with self.db:
            if await self.get_message_id(chat_id):
                self.sql.execute(f"UPDATE messages SET message_id={message_id} WHERE chat_id={chat_id}")
            else:

                self.sql.execute(f"INSERT INTO messages(chat_id, message_id) VALUES({chat_id}, {message_id})")

    async def del_message_id(self, chat_id):
        with self.db:
            self.sql.execute(f"DELETE FROM messages WHERE chat_id = {chat_id}")

    async def get_message_id(self, chat_id):
        self.sql.execute(f"SELECT message_id FROM messages WHERE chat_id={chat_id}")
        message_id = self.sql.fetchone()
        if message_id:
            return message_id[0]
        else:
            return None

    async def add_new_user(self, user_id, username):
        with self.db:
            if await self.get_user(user_id):
                self.sql.execute(f"UPDATE users SET username='{username}' "
                                 f"WHERE user_id={user_id}")
            else:
                self.sql.execute(f"INSERT INTO users(user_id, username) "
                                 f"VALUES({user_id}, '{username}')")

    async def add_new_sale(self, user_id, number):
        with self.db:
            self.sql.execute(f"INSERT INTO sales(user_id, numbers) VALUES({user_id}, ARRAY{number})")

    async def update_sales(self, user_id, number):
        with self.db:
            self.sql.execute(f"UPDATE sales SET numbers = ARRAY{number} WHERE user_id={user_id}")

    async def delete_sale(self, user_id):
        with self.db:
            self.sql.execute(f"DELETE FROM sales WHERE user_id = {user_id}")

    async def add_new_item(self, title, text, callback_data):
        with self.db:
            self.sql.execute(f"INSERT INTO menu_items(title, description, callback_data)"
                             f"VALUES('{title}', '{text}', '{callback_data}')")

    async def add_new_text(self, item_id, text):
        with self.db:
            self.sql.execute(f"UPDATE menu_items SET description = '{text}' WHERE id={item_id}")

    async def add_new_content(self, callback_data, file):
        with self.db:
            self.sql.execute(f"INSERT INTO files(file_id, callback_data) VALUES ('{file}', '{callback_data}')")
            self.sql.execute(f"UPDATE menu_items SET files = 1 WHERE callback_data = '{callback_data}'")

    async def update_content(self, callback_data, file):
        with self.db:
            self.sql.execute(f"DELETE FROM files WHERE callback_data='{callback_data}'")
            self.sql.execute(f"INSERT INTO files(file_id, callback_data) VALUES ('{file}', '{callback_data}')")
            self.sql.execute(f"UPDATE menu_items SET files = 1 WHERE callback_data = '{callback_data}'")

    async def del_sale(self, user_id, numbers):
        with self.db:
            self.sql.execute(f"DELETE FROM sales WHERE user_id = {user_id} AND numbers = '{numbers}'")

    # Getters

    async def get_languages(self):
        self.sql.execute("SELECT * FROM languages")
        return self.sql.fetchall()

    async def get_russian_texts(self):
        self.sql.execute("SELECT * FROM ru WHERE file_id == null")
        return self.sql.fetchall()

    async def get_user(self, user_id):
        self.sql.execute(f"SELECT * FROM users WHERE user_id={user_id}")
        return self.sql.fetchone()

    async def get_sales(self, user_id):
        self.sql.execute(f"SELECT numbers FROM sales WHERE user_id={user_id}")
        return self.sql.fetchone()

    async def get_menu_items(self):
        self.sql.execute(f"SELECT * FROM menu_items")
        return self.sql.fetchall()

    async def get_subsections(self, callback_data):
        if callback_data:
            self.sql.execute(f"SELECT * FROM subsections WHERE callback_data='{callback_data}'")
            return self.sql.fetchall()
        return None

    async def get_sub_subsections(self, callback_data):
        if callback_data:
            self.sql.execute(f"SELECT * FROM sub_subsections WHERE callback_data='{callback_data}'")
            return self.sql.fetchall()
        return None

    async def get_item_text(self, callback_data):
        self.sql.execute(f"SELECT description FROM menu_items WHERE callback_data='{callback_data}'")
        return self.sql.fetchone()[0]

    async def get_subsection_text(self, callback_data):
        self.sql.execute(f"SELECT description FROM subsections WHERE sub_call_data='{callback_data}'")
        return self.sql.fetchone()[0]

    async def get_sub_subsection_text(self, callback_data):
        self.sql.execute(f"SELECT description FROM sub_subsections WHERE call_data='{callback_data}'")
        return self.sql.fetchone()[0]

    async def get_files(self, callback_data, lang):
        self.sql.execute(
            f"SELECT file_id, callback_data FROM files WHERE callback_data='{callback_data}' AND (language='{lang}' OR language IS "
            f"NULL) ORDER BY id")
        return self.sql.fetchall()

    async def get_users(self):
        self.sql.execute("SELECT user_id FROM users")
        return self.sql.fetchall()

    async def get_sale(self, user_id, number):
        sales = await self.get_sales(user_id)
        print(sales)

        if sales:
            if number in sales[0]:
                return number
        return None



