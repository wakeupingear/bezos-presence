from distutils.core import setup
import py2exe
setup(
    console=["bezos.py"],
    options={"py2exe": {
        "bundle_files": 1, "compressed": True, "optimize": 2,
    }},
    name="BezosPresence",
    version="1.0.0"
)
