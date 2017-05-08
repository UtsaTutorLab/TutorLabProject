from distutils.core import setup
import py2exe

setup(
    name = "TutorLab",
    version = "0.9",
    author =  "Koby Huckabee",
    license = "GNU General Public License (GPL)",
    packages = ['TutorLabPyApp'],
    package_data = {"TutorLabPyApp": ["ui/*"]},
    windows = [{"script": "bin/TutorLabPyApp"}],
    options = {"py2exe": {"skip_archive": True, "includes":["sip"]}}
)