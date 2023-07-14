# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_thumb.ipynb.

# %% auto 0
__all__ = ['get_img', 'img2thumb', 'nb2thumb']

# %% ../nbs/00_thumb.ipynb 2
import io, base64, re
import nbformat
from PIL import Image
from fastcore.foundation import L
from fastcore.test import test_fail
from io import BytesIO

# %% ../nbs/00_thumb.ipynb 4
def _decode_img(base64_str):
    img = Image.open(BytesIO(base64.b64decode(base64_str)))
    if img.mode == "RGBA":
        img = img.convert("RGB")
    return img

def get_img(nb_path, label='thumbnail'):
    "Get image from notebook with a quarto cell directive with `#|label: {label}`"
    out_plots = None
    lbl = re.compile(f'#\|(\s*)label:(\s*){label}')
    nb = nbformat.read(open(nb_path), as_version=4)
    for cell in nb.cells:
        if lbl.search(cell.source):
            out_plots = [x for x in cell.outputs if x.output_type == "display_data" and 'data' in x]
            if out_plots:
                data = out_plots[0]['data']
                if 'image/png' not in data: 
                    raise Exception(f'{nb_path}: thumbnails are only supported for `image/png`, found {data.keys()}')
                return _decode_img(data['image/png'])
            else:
                raise Exception(f'{nb_path}: cell with `#|label: {label}` does not have an output type of `display_data`')
    if out_plots is None:
        raise Exception(f'{nb_path} does not contain a cell with `#|label: {label}`')

# %% ../nbs/00_thumb.ipynb 9
def img2thumb(img:Image.Image, size=(260,260)):
    "Convert image to thumbnail."
    thumb_size = size[0] * 2, size[1] * 2
    img.thumbnail(thumb_size)
    return img

# %% ../nbs/00_thumb.ipynb 12
def nb2thumb(nb_path, label='thumbnail', size=(260,260)) -> Image.Image:
    "Extract thumbnail corresponding to the cell with the comment `#|label: {label}` from a notebook."
    img = get_img(nb_path=nb_path, label=label)
    return img2thumb(img, size=size)
