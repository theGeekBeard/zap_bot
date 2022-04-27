import json

from supabase import create_client, Client


class Database:

    def __init__(self, URL, KEY):
        self.db: Client = create_client(URL, KEY)

    # Getters

    async def get_passes(self, person_id):
        data = self.db.table("passes").select("holder_name", "title", "id").eq("requested_by", person_id).execute()
        return data.data

    async def get_person_id(self, user_id):
        data = self.db.table("persons").select("id").eq("telegram_id", user_id).execute()
        return data.data

    async def get_pass(self, pass_id):
        data = self.db.table("passes").select("end_date", "status", "created_date", "start_date").eq("id",
                                                                                                     pass_id).execute()
        return data.data

    async def get_user(self, user_id):
        data = self.db.table("users").select("*").eq("user_id", user_id).execute()
        return data.data

    async def get_sales(self, user_id):
        data = self.db.table("sales").select("numbers").eq("user_id", user_id).execute()
        if not data.data:
            return None
        aList = json.loads(data.data[0]["numbers"])
        return aList

    async def get_users(self):
        data = self.db.table("users").select("user_id").execute()
        return data.data

    async def get_sale(self, user_id, number):
        sales = await self.get_sales(user_id)

        if sales:
            if number in sales[0]:
                return number
        return None

    async def get_index(self, chat_id):
        data = self.db.table("navigation").select("index").eq("chat_id", chat_id).execute()
        return data.data[0]["index"] if data.data else None

    async def get_message_id(self, chat_id):
        data = self.db.table("messages").select("message_id").eq("chat_id", chat_id).execute()
        return data.data[0]["message_id"] if data.data else None

    # Setters
    async def add_index(self, chat_id, index):
        data = {
            "chat_id": chat_id,
            "index": index
        }

        if await self.get_index(chat_id) is not None:
            self.db.table("navigation").update(data).eq("chat_id", chat_id).execute()
        else:
            self.db.table("navigation").insert(data).execute()

    async def del_index(self, chat_id):
        self.db.table("navigation").delete().eq("chat_id", chat_id).execute()

    async def add_message_id(self, chat_id, message_id):
        data = {
            "chat_id": chat_id,
            "message_id": message_id
        }

        if await self.get_message_id(chat_id):
            self.db.table("messages").update({"message_id": message_id}).eq("chat_id", chat_id).execute()
        else:
            self.db.table("messages").insert(data).execute()

    async def del_message_id(self, chat_id):
        self.db.table("messages").delete().eq("chat_id", chat_id).execute()

    async def add_new_user(self, user_id, username):
        data = {
            "user_id": user_id,
            "username": username
        }

        if await self.get_user(user_id):
            self.db.table("users").update({"username": username}).eq("user_id", user_id).execute()
        else:
            self.db.table("users").insert(data).execute()

    async def add_new_sale(self, user_id, number):
        data = {
            "user_id": user_id,
            "numbers": number
        }

        self.db.table("sales").insert(data).execute()

    async def update_sales(self, user_id, number):
        self.db.table("sales").update({"numbers": number}).eq("user_id", user_id).execute()

    async def delete_sale(self, user_id):
        self.db.table("sales").delete().eq("user_id", user_id).execute()

    async def del_sale(self, user_id, numbers):
        self.db.table("sales").delete().match({"user_id": user_id, "numbers": numbers}).execute()

# class Database:
#

#     def __init__(self, url, key):
#         self.db = con
#         self.sql = self.db.cursor()
#
#     # Setters
#     async def add_index(self, chat_id, index):
#         with self.db:
#             if await self.get_index(chat_id) is not None:
#                 self.sql.execute(f"UPDATE navigation SET index={index} WHERE chat_id={chat_id}")
#             else:
#                 self.sql.execute(f"INSERT INTO navigation(chat_id, index) VALUES({chat_id}, {index})")
#
#     async def del_index(self, chat_id):
#         with self.db:
#             self.sql.execute(f"DELETE FROM navigation WHERE chat_id = {chat_id}")
#
#     async def get_index(self, chat_id):
#         self.sql.execute(f"SELECT index FROM navigation WHERE chat_id={chat_id}")
#         index = self.sql.fetchone()
#         print(index)
#         if index:
#             return index[0]
#         else:
#             return None
#
#     async def add_message_id(self, chat_id, message_id):
#         with self.db:
#             if await self.get_message_id(chat_id):
#                 self.sql.execute(f"UPDATE messages SET message_id={message_id} WHERE chat_id={chat_id}")
#             else:
#
#                 self.sql.execute(f"INSERT INTO messages(chat_id, message_id) VALUES({chat_id}, {message_id})")
#
#     async def del_message_id(self, chat_id):
#         with self.db:
#             self.sql.execute(f"DELETE FROM messages WHERE chat_id = {chat_id}")
#
#     async def get_message_id(self, chat_id):
#         self.sql.execute(f"SELECT message_id FROM messages WHERE chat_id={chat_id}")
#         message_id = self.sql.fetchone()
#         if message_id:
#             return message_id[0]
#         else:
#             return None
#
#     async def add_new_user(self, user_id, username):
#         with self.db:
#             if await self.get_user(user_id):
#                 self.sql.execute(f"UPDATE users SET username='{username}' "
#                                  f"WHERE user_id={user_id}")
#             else:
#                 self.sql.execute(f"INSERT INTO users(user_id, username) "
#                                  f"VALUES({user_id}, '{username}')")
#
#     async def add_new_sale(self, user_id, number):
#         with self.db:
#             self.sql.execute(f"INSERT INTO sales(user_id, numbers) VALUES({user_id}, ARRAY{number})")
#
#     async def update_sales(self, user_id, number):
#         with self.db:
#             self.sql.execute(f"UPDATE sales SET numbers = ARRAY{number} WHERE user_id={user_id}")
#
#     async def delete_sale(self, user_id):
#         with self.db:
#             self.sql.execute(f"DELETE FROM sales WHERE user_id = {user_id}")
#
#     async def add_new_item(self, title, text, callback_data):
#         with self.db:
#             self.sql.execute(f"INSERT INTO menu_items(title, description, callback_data)"
#                              f"VALUES('{title}', '{text}', '{callback_data}')")
#
#     async def add_new_text(self, item_id, text):
#         with self.db:
#             self.sql.execute(f"UPDATE menu_items SET description = '{text}' WHERE id={item_id}")
#
#     async def add_new_content(self, callback_data, file):
#         with self.db:
#             self.sql.execute(f"INSERT INTO files(file_id, callback_data) VALUES ('{file}', '{callback_data}')")
#             self.sql.execute(f"UPDATE menu_items SET files = 1 WHERE callback_data = '{callback_data}'")
#
#     async def update_content(self, callback_data, file):
#         with self.db:
#             self.sql.execute(f"DELETE FROM files WHERE callback_data='{callback_data}'")
#             self.sql.execute(f"INSERT INTO files(file_id, callback_data) VALUES ('{file}', '{callback_data}')")
#             self.sql.execute(f"UPDATE menu_items SET files = 1 WHERE callback_data = '{callback_data}'")
#
#     async def del_sale(self, user_id, numbers):
#         with self.db:
#             self.sql.execute(f"DELETE FROM sales WHERE user_id = {user_id} AND numbers = '{numbers}'")
#
#     # Getters
#
#     async def get_user(self, user_id):
#         self.sql.execute(f"SELECT * FROM users WHERE user_id={user_id}")
#         return self.sql.fetchone()
#
#     async def get_sales(self, user_id):
#         self.sql.execute(f"SELECT numbers FROM sales WHERE user_id={user_id}")
#         return self.sql.fetchone()
#
#     async def get_users(self):
#         self.sql.execute("SELECT user_id FROM users")
#         return self.sql.fetchall()
#
#     async def get_sale(self, user_id, number):
#         sales = await self.get_sales(user_id)
#
#         if sales:
#             if number in sales[0]:
#                 return number
#         return None
