Bottle on OpenShift Express
============================

This git repository helps you get up and running quickly w/ a Bottle installation
on OpenShift Express.


Running on OpenShift
----------------------------

Create an account at http://openshift.redhat.com/

Create a wsgi-3.2 application

    rhc-create-app -a bottle -t wsgi-3.2

Add this upstream bottle repo

    cd bottle
    git remote add upstream -m master git://github.com/openshift/bottle-openshift-quickstart.git
    git pull -s recursive -X theirs upstream master
    
Then push the repo upstream

    git push

That's it, you can now checkout your application at:

    http://bottle-$yournamespace.rhcloud.com

