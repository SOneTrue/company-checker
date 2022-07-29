from aiogram.types import MediaGroup


async def make_album(state):
    user_data = await state.get_data()
    photo_one = user_data['photo_one']
    photo_two = user_data['photo_two']
    photo_three = user_data['photo_three']
    photo_four = user_data['photo_four']
    photo_five = user_data['photo_five']
    photo_six = user_data['photo_six']
    album = MediaGroup()
    album.attach_photo(photo_one)
    album.attach_photo(photo_two)
    album.attach_photo(photo_three)
    album.attach_photo(photo_four)
    album.attach_photo(photo_five)
    album.attach_photo(photo_six)
    return album
