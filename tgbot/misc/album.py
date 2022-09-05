from aiogram.types import MediaGroup


async def make_album(state):
    user_data = await state.get_data()
    album = MediaGroup()
    album.attach_photo(user_data['photo_one'])
    album.attach_photo(user_data['photo_two'])
    album.attach_photo(user_data['photo_three'])
    album.attach_photo(user_data['photo_four'])
    album.attach_photo(user_data['photo_five'])
    album.attach_photo(user_data['photo_six'])
    return album
