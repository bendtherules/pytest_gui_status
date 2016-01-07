import os
import tempfile
import shutil


class patched_chdir(object):

    """Just like chdir, but can be used in  `with` - sets back the old path at exit"""

    def __init__(self, new_path):
        self.old_path = os.getcwd()
        self.new_path = new_path

    def __enter__(self):
        os.chdir(self.new_path)

    def __exit__(self, type, value, traceback):
        os.chdir(self.old_path)


def create_temp_case(case_name, case_basedir=None, path_tmpdir=None):
    case_basedir = case_basedir or __file__
    with patched_chdir(os.path.dirname(case_basedir)):
        path_test_cases = os.path.abspath("../testcases/")
        path_case = os.path.join(path_test_cases, case_name)

        path_tmpdir = path_tmpdir or tempfile.mkdtemp()
        path_tmpdir_case = os.path.join(path_tmpdir, case_name)
        shutil.copytree(path_case, path_tmpdir_case)

    return path_tmpdir_case


def reload_2_3(module_name):
    '''
    reload that works in all versions of Python.
    Uses builtin reload in py2, imp.reload for <=py3.3,
    importlib.reload for >=3.4

    The module six has similar functionalities,
    but would be too huge a dependency for this simple case.
    '''

    from sys import version_info
    major_ver, minor_ver = version_info[:2]

    if major_ver == 2:
        reload(module_name)
    elif major_ver == 3 and minor_ver <= 3:
        import imp
        imp.reload(module_name)
    elif major_ver == 3 and minor_ver >= 4:
        import importlib
        importlib.reload(module_name)
    else:
        raise NotImplementedError("Not sure how to reload in "
                                  "this version of Python, supported upto 3.x")
