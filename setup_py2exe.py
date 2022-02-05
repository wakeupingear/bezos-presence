from distutils.core import setup
import py2exe
setup(
    console=["bezos.py"],
    options={"py2exe": {
        "bundle_files": 3, "compressed": True, "optimize": 0,
    }},
    name="BezosPresence",
    version="1.0.0"
)
