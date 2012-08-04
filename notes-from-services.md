# README for a newly created project.

There are a couple of things you should do first, before you can use all of Git's power:

  * Add a remote to this project: in the Cloud9 IDE command line, you can execute the following commands
    `git remote add [remote name] [remote url (eg. 'git@github.com:/ajaxorg/node_chat')]` [Enter]
  * Create new files inside your project
  * Add them to to Git by executing the following command
    `git add [file1, file2, file3, ...]` [Enter]
  * Create a commit which can be pushed to the remote you just added
    `git commit -m 'added new files'` [Enter]
  * Push the commit the remote
    `git push [remote name] master` [Enter]

That's it! If this doesn't work for you, please visit the excellent resources from [Github.com](http://help.github.com) and the [Pro Git](http://http://progit.org/book/) book.
If you can't find your answers there, feel free to ask us via Twitter (@cloud9ide), [mailing list](groups.google.com/group/cloud9-ide) or IRC (#cloud9ide on freenode).

Happy coding!


Feel free to change or remove this file, it is informational only.

Repo layout
===========
wsgi/ - Externally exposed wsgi code goes
wsgi/static/ - Public static content gets served here
libs/ - Additional libraries
data/ - For not-externally exposed wsgi code
setup.py - Standard setup.py, specify deps here
../data - For persistent data (also env var: OPENSHIFT_DATA_DIR)
.openshift/action_hooks/pre_build - Script that gets run every git push before the build
.openshift/action_hooks/build - Script that gets run every git push as part of the build process (on the CI system if available)
.openshift/action_hooks/deploy - Script that gets run every git push after build but before the app is restarted
.openshift/action_hooks/post_deploy - Script that gets run every git push after the app is restarted


Environment Variables
=====================

OpenShift provides several environment variables to reference for ease
of use.  The following list are some common variables but far from exhaustive:

    os.environ['OPENSHIFT_GEAR_NAME']  - Application name
    os.environ['OPENSHIFT_GEAR_DIR']   - Application dir
    os.environ['OPENSHIFT_DATA_DIR']  - For persistent storage (between pushes)
    os.environ['OPENSHIFT_TMP_DIR']   - Temp storage (unmodified files deleted after 10 days)

When embedding a database using 'rhc app cartridge add', you can reference environment
variables for username, host and password:

    os.environ['OPENSHIFT_DB_HOST']      - DB host
    os.environ['OPENSHIFT_DB_PORT']      - DB Port
    os.environ['OPENSHIFT_DB_USERNAME']  - DB Username
    os.environ['OPENSHIFT_DB_PASSWORD']  - DB Password

To get a full list of environment variables, simply add a line in your
.openshift/action_hooks/build script that says "export" and push.


Notes about layout
==================
Please leave wsgi, libs and data directories but feel free to create additional
directories if needed.

Note: Every time you push, everything in your remote repo dir gets recreated
please store long term items (like an sqlite database) in ../data which will
persist between pushes of your repo.


Notes about setup.py
====================

Adding deps to the install_requires will have the openshift server actually
install those deps at git push time.
