from urllib.request import urlopen

from orderedsets import __version__

_conf_url = \
    "https://raw.githubusercontent.com/inducer/sphinxconfig/main/sphinxconfig.py"
with urlopen(_conf_url) as _inf:
    exec(compile(_inf.read(), _conf_url, "exec"), globals())

project = "orderedsets"
copyright = "2023, University of Illinois Board of Trustees"
author = "Orderedsets contributors"
version = __version__
release = __version__

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "immutabledict": ("https://immutabledict.corenting.fr/", None)
}
