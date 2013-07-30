from sage.env import SAGE_DOT_GIT, SAGE_REPO_AUTHENTICATED, SAGE_SRC

from git_error import GitError

SILENT = object()
SUPER_SILENT = object()
READ_OUTPUT = object()
        sage: from sage.dev.config import Config
        sage: from sage.dev.user_interface import UserInterface
        sage: config = Config()
        sage: GitInterface(config, UserInterface(config))
        GitInterface()
            sage: from sage.dev.config import Config
            sage: from sage.dev.user_interface import UserInterface
            sage: config = Config()
            sage: type(GitInterface(config, UserInterface(config)))
            <class 'sage.dev.git_interface.GitInterface'>
        self._src = self._config.get('src', SAGE_SRC)
        Return a printable representation of this object.
            sage: from sage.dev.config import Config
            sage: from sage.dev.user_interface import UserInterface
            sage: from sage.dev.git_interface import GitInterface
            sage: config = Config()
            sage: repr(GitInterface(config, UserInterface(config)))

        OUTPUT:
        EXAMPLES:
        Create a :class:`GitInterface` for doctesting::

            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create two conflicting branches::

            sage: os.chdir(config['git']['src'])
            sage: with open("file","w") as f: f.write("version 0")
            sage: git.add("file")
            sage: git.commit(SUPER_SILENT, "-m","initial commit")
            sage: git.checkout(SUPER_SILENT, "-b","branch1")
            sage: with open("file","w") as f: f.write("version 1")
            sage: git.commit(SUPER_SILENT, "-am","second commit")
            sage: git.checkout(SUPER_SILENT, "master")
            sage: git.checkout(SUPER_SILENT, "-b","branch2")
            sage: with open("file","w") as f: f.write("version 2")
            sage: git.commit(SUPER_SILENT, "-am","conflicting commit")

        A ``merge`` state::

            sage: git.checkout(SUPER_SILENT, "branch1")
            sage: git.merge(SUPER_SILENT, 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1)
            sage: git.merge(SUPER_SILENT,abort=True)

        A ``rebase`` state::

            sage: git.execute_supersilent('rebase', 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1)
            sage: git.rebase(SUPER_SILENT, abort=True)

        A merge within an interactive rebase::

            sage: git.rebase(SUPER_SILENT, 'HEAD^', interactive=True, env={'GIT_SEQUENCE_EDITOR':'sed -i s+pick+edit+'})
            sage: git.merge(SUPER_SILENT, 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1)
            sage: git.rebase(SUPER_SILENT, abort=True)
        Get out of a merge/am/rebase/etc state.
        EXAMPLES:
        Create a :class:`GitInterface` for doctesting::

            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create two conflicting branches::

            sage: os.chdir(config['git']['src'])
            sage: with open("file","w") as f: f.write("version 0")
            sage: git.add("file")
            sage: git.commit(SUPER_SILENT, "-m","initial commit")
            sage: git.checkout(SUPER_SILENT, "-b","branch1")
            sage: with open("file","w") as f: f.write("version 1")
            sage: git.commit(SUPER_SILENT, "-am","second commit")
            sage: git.checkout(SUPER_SILENT, "master")
            sage: git.checkout(SUPER_SILENT, "-b","branch2")
            sage: with open("file","w") as f: f.write("version 2")
            sage: git.commit(SUPER_SILENT, "-am","conflicting commit")

        A merge within an interactive rebase::

            sage: git.checkout(SUPER_SILENT, "branch1")
            sage: git.rebase(SUPER_SILENT, 'HEAD^', interactive=True, env={'GIT_SEQUENCE_EDITOR':'sed -i s+pick+edit+'})
            ('rebase-i',)
            sage: git.merge(SUPER_SILENT, 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1)

        Get out of this state::

            sage: git.reset_to_clean_state()

            return
        Reset any changes made to the working directory.
        INPUT:

        - ``remove_untracked_files`` -- a boolean (default: ``False``), whether
          to remove files which are not tracked by git

        - ``remove_untracked_directories`` -- a boolean (default: ``False``),
          whether to remove directories which are not tracked by git

        - ``remove_ignored`` -- a boolean (default: ``False``), whether to
          remove files directories which are ignored by git

        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Set up some files/directories::

            sage: os.chdir(config['git']['src'])
            sage: open('tracked','w').close()
            sage: git.add(SUPER_SILENT, 'tracked')
            sage: with open('.gitignore','w') as f: f.write('ignored\nignored_dir')
            sage: git.add(SUPER_SILENT, '.gitignore')
            sage: git.commit(SUPER_SILENT, '-m', 'initial commit')

            sage: os.mkdir('untracked_dir')
            sage: open('untracked_dir/untracked','w').close()
            sage: open('untracked','w').close()
            sage: open('ignored','w').close()
            sage: os.mkdir('ignored_dir')
            sage: open('ignored_dir/untracked','w').close()
            sage: with open('tracked','w') as f: f.write('version 0')
            sage: git.status()
            # On branch master
            # Changes not staged for commit:
            #   (use "git add <file>..." to update what will be committed)
            #   (use "git checkout -- <file>..." to discard changes in working directory)
            #
            #   modified:   tracked
            #
            # Untracked files:
            #   (use "git add <file>..." to include in what will be committed)
            #
            #   untracked
            #   untracked_dir/
            no changes added to commit (use "git add" and/or "git commit -a")

        Some invalid combinations of flags::

            sage: git.reset_to_clean_working_directory(remove_untracked_files = False, remove_untracked_directories = True)
            Traceback (most recent call last):
            ...
            ValueError: remove_untracked_directories only valid if remove_untracked_files is set
            sage: git.reset_to_clean_working_directory(remove_untracked_files = False, remove_ignored = True)
            Traceback (most recent call last):
            ...
            ValueError: remove_ignored only valid if remove_untracked_files is set

        Per default only the tracked modified files are reset to a clean
        state::

            sage: git.reset_to_clean_working_directory()
            sage: git.status()
            # On branch master
            # Untracked files:
            #   (use "git add <file>..." to include in what will be committed)
            #
            #   untracked
            #   untracked_dir/
            nothing added to commit but untracked files present (use "git add" to track)

        Untracked items can be removed by setting the parameters::

            sage: git.reset_to_clean_working_directory(remove_untracked_files=True)
            Removing untracked
            Not removing untracked_dir/
            sage: git.reset_to_clean_working_directory(remove_untracked_files=True, remove_untracked_directories=True)
            Removing untracked_dir/
            sage: git.reset_to_clean_working_directory(remove_untracked_files=True, remove_ignored=True)
            Removing ignored
            Not removing ignored_dir/
            sage: git.reset_to_clean_working_directory(remove_untracked_files=True, remove_untracked_directories=True, remove_ignored=True)
            Removing ignored_dir/

        if remove_untracked_directories and not remove_untracked_files:
            raise ValueError("remove_untracked_directories only valid if remove_untracked_files is set")
        if remove_ignored and not remove_untracked_files:
            raise ValueError("remove_ignored only valid if remove_untracked_files is set")

        self.reset(SILENT, hard=True)
        Common implementation for :meth:`execute`, :meth:`execute_silent`,
        :meth:`execute_supersilent`, and :meth:`read_output`
          - ``stdout`` - if set to ``False`` will supress stdout
          - ``stderr`` - if set to ``False`` will supress stderr
            sage: import os
            sage: from sage.dev.git_interface import GitInterface
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config['git']['src'])

            sage: git._run_git('status', (), {})
            # On branch master
            # Initial commit
            #
            nothing to commit (create/copy files and use "git add" to track)

        TESTS:

        Check that we refuse to touch the live source code in doctests::

            sage: dev.git.status()
            Traceback (most recent call last):
            ...
            AssertionError: attempt to work with the live repository or directory in a doctest

        import sage.doctest
        import os
        assert not sage.doctest.DOCTEST_MODE or (self._dot_git != SAGE_DOT_GIT and self._repository != SAGE_REPO_AUTHENTICATED and os.path.abspath(os.getcwd()).startswith(self._src)), "attempt to work with the live repository or directory in a doctest"
        from sage.dev.user_interface import INFO
        self._UI.show("[git] %s"%(" ".join(s)), log_level=INFO)
        import subprocess
        - ``cmd`` - git command run
        - ``args`` - extra arguments for git
        - ``kwds`` - extra keywords for git
            sage: import os
            sage: from sage.dev.git_interface import GitInterface
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config['git']['src'])

            sage: git.execute('status')
            # On branch master
            # Initial commit
            nothing to commit (create/copy files and use "git add" to track)
            sage: git.execute_silent('status',foo=True) # --foo is not a valid parameter
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (129)

            sage: import os
            sage: from sage.dev.git_interface import GitInterface
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config['git']['src'])

            sage: git.execute_silent('status',foo=True) # --foo is not a valid parameter
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (129)

            sage: import os
            sage: from sage.dev.git_interface import GitInterface
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config['git']['src'])

            sage: git.execute_supersilent('status',foo=True) # --foo is not a valid parameter
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (129)

            sage: import os
            sage: from sage.dev.git_interface import GitInterface
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))
            sage: os.chdir(config['git']['src'])

            sage: git.read_output('status')
            '# On branch master\n#\n# Initial commit\n#\nnothing to commit (create/copy files and use "git add" to track)\n'
            sage: git.read_output('status',foo=True) # --foo is not a valid parameter
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (129)

        Return whether ``a`` is a child of ``b``.
        EXAMPLES:
        Create a :class:`GitInterface` for doctesting::

            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create two conflicting branches::

            sage: os.chdir(config['git']['src'])
            sage: with open("file","w") as f: f.write("version 0")
            sage: git.add("file")
            sage: git.commit(SUPER_SILENT, "-m","initial commit")
            sage: git.checkout(SUPER_SILENT, "-b","branch1")
            sage: with open("file","w") as f: f.write("version 1")
            sage: git.commit(SUPER_SILENT, "-am","second commit")
            sage: git.checkout(SUPER_SILENT, "master")
            sage: git.checkout(SUPER_SILENT, "-b","branch2")
            sage: with open("file","w") as f: f.write("version 2")
            sage: git.commit(SUPER_SILENT, "-am","conflicting commit")

            sage: git.is_child_of('master', 'branch2')
            sage: git.is_child_of('branch2', 'master')
            sage: git.is_child_of('branch1', 'branch2')
            False
            sage: git.is_child_of('master', 'master')

        Return whether ``a`` is an ancestor of ``b``.
        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::
            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create two conflicting branches::

            sage: os.chdir(config['git']['src'])
            sage: with open("file","w") as f: f.write("version 0")
            sage: git.add("file")
            sage: git.commit(SUPER_SILENT, "-m","initial commit")
            sage: git.checkout(SUPER_SILENT, "-b","branch1")
            sage: with open("file","w") as f: f.write("version 1")
            sage: git.commit(SUPER_SILENT, "-am","second commit")
            sage: git.checkout(SUPER_SILENT, "master")
            sage: git.checkout(SUPER_SILENT, "-b","branch2")
            sage: with open("file","w") as f: f.write("version 2")
            sage: git.commit(SUPER_SILENT, "-am","conflicting commit")

            sage: git.is_ancestor_of('master', 'branch2')
            sage: git.is_ancestor_of('branch2', 'master')
            False
            sage: git.is_ancestor_of('branch1', 'branch2')
            sage: git.is_ancestor_of('master', 'master')

        return not self.rev_list(READ_OUTPUT, '{}..{}'.format(b, a)).splitlines()
        Return whether there are uncommitted changes, i.e., whether there are
        modified files which are tracked by git.
        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        An untracked file does not count towards uncommited changes::

            sage: os.chdir(config['git']['src'])
            sage: open('untracked','w').close()
        Once added to the index it does::
            sage: git.add('untracked')
            sage: git.commit(SUPER_SILENT, '-m', 'tracking untracked')
            sage: with open('untracked','w') as f: f.write('version 0')
            sage: git.has_uncommitted_changes()
            True

        return bool([line for line in self.status(READ_OUTPUT, porcelain=True).splitlines() if not line.startswith('?')])
    def untracked_files(self):
        Return a list of file names for files that are not tracked by git and
        not ignored.
        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::

            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        An untracked file::

            sage: os.chdir(config['git']['src'])
            sage: git.untracked_files()
            []
            sage: open('untracked','w').close()
            sage: git.untracked_files()
            ['untracked']

         Directories are not displayed here::

            sage: os.mkdir('untracked_dir')
            sage: git.untracked_files()
            ['untracked']
            sage: open('untracked_dir/untracked','w').close()
            sage: git.untracked_files()
            ['untracked', 'untracked_dir/untracked']
        return self.read_output('ls-files', other=True, exclude_standard=True).splitlines()
for git_cmd_ in (
        "init",
        "rev_list",
        "tag"
    def create_wrapper(git_cmd__):
        r"""
        Create a wrapper for `git_cmd__`.

        EXAMPLES::
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: from sage.dev.git_interface import GitInterface
            sage: GitInterface(DoctestConfig(), DoctestUserInterface()).status()

        """
        git_cmd = git_cmd__.replace("_","-")
        def meth(self, *args, **kwds):
            r"""
            Call `git {0}`.

            If `args` contains ``SILENT``, then output to stdout is supressed.

            If `args` contains ``SUPER_SILENT``, then output to stdout and stderr
            is supressed.

            OUTPUT:

            Returns ``None`` unless `args` contains ``READ_OUTPUT``; in that case,
            the commands output to stdout is returned.

            See :meth:`execute` for more information.

            EXAMPLES:

                sage: dev.git.{1}() # not tested

            """.format(git_cmd, git_cmd__)
            args = list(args)
            if len([arg for arg in args if arg in (SILENT, SUPER_SILENT, READ_OUTPUT)]) > 1:
                raise ValueError("at most one of SILENT, SUPER_SILENT, READ_OUTPUT allowed")
            if SILENT in args:
                args.remove(SILENT)
                return self.execute_silent(git_cmd, *args, **kwds)
            elif SUPER_SILENT in args:
                args.remove(SUPER_SILENT)
                return self.execute_supersilent(git_cmd, *args, **kwds)
            elif READ_OUTPUT in args:
                args.remove(READ_OUTPUT)
                return self.read_output(git_cmd, *args, **kwds)
            else:
                return self.execute(git_cmd, *args, **kwds)
        return meth
    setattr(GitInterface, git_cmd_, create_wrapper(git_cmd_))