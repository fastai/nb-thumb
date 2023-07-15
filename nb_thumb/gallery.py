# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_gallery.ipynb.

# %% auto 0
__all__ = ['emb_img', 'gallery']

# %% ../nbs/01_gallery.ipynb 2
from .thumb import nb2thumb
from pathlib import Path
from fastcore.foundation import L
from fastcore.utils import mkdir
from fastcore.test import test_eq

# %% ../nbs/01_gallery.ipynb 3
def emb_img(nb_path:str, # the path to the notebook
            label:str, # the label indicating the cell where the plot is
            caption:str='', # the caption, will be inferred from label if not specified.
            anchor='#example', # anchor tag in source page, this defaults to `#example` for plotnine: https://plotnine.readthedocs.io
           size=(150,150) # size of the thumbnail
           ) -> str:
    "Embed a thumbnail image as a markdown cell."
    if not caption: caption = label.replace('_', ' ').title()
    d = mkdir(f'{Path(nb_path).stem}_data', exist_ok=True)
    img = nb2thumb(nb_path, label=label, size=size)
    outfile = d/f'{label}.png'
    img.save(outfile)
    
    return f"""
::: {{.g-col-6 .g-col-md-6 .mb-4 .border .rounded .shadow-sm .d-flex .flex-column .justify-content-center .align-items-center .px-3}}

![]({outfile}){{.plot-gallery}}

[{caption}]({nb_path}{anchor})

:::
""" 

# %% ../nbs/01_gallery.ipynb 8
def gallery(plots:list[dict] # a list of dictionaries which contain arguments for `emb_img`.
           ) -> str:
    "Arrange plots into a gallery."
    md = L(plots).map(lambda x: emb_img(**x))
    return '\n::: {.content-block .grid .gap-4}\n' + '\n'.join(md) + '\n:::'
        
