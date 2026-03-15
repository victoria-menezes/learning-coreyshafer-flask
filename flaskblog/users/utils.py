# from flaskblog import app
from flask import current_app as app

import secrets
import os

from PIL import Image

def save_picture(
    form_picture,
    output_size : tuple[int, int] = (125, 125)
    ):
    # randomize new name for the file
    random_hex = secrets.token_hex(8)
    
    # grab file extension
    _, f_ext = os.path.splitext(form_picture.filename)

    # final file name
    picture_fn = random_hex + f_ext

    # full path of where the image will be saved
    picture_path = os.path.join(
        app.root_path,
        'static/profile_pics',
        picture_fn
        )
    
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    
    img.save(picture_path)
    
    return picture_fn

def send_reset_email(user): # unimplemented
    pass
