from aiogram.types import MediaGroup


async def make_album(photo_one, photo_two, photo_three, photo_four, photo_five, photo_six):
    album = MediaGroup()
    album.attach_photo(photo_one)
    album.attach_photo(photo_two)
    album.attach_photo(photo_three)
    album.attach_photo(photo_four)
    album.attach_photo(photo_five)
    album.attach_photo(photo_six)
    return album
