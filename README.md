# gitlog-visualizer

A simple way to use [gource](http://gource.io/) to show your git's repo history as a nice visualization

## Some useful stuff

- [Using captions](https://github.com/acaudwell/Gource/wiki/Captions)

### Renaming commiters

Sometimes, the same commiter did some changes under different name/email configurations, and you might want to merge them into one. To do so, you can run something like

    git filter-branch --env-filter '
    if [ "$GIT_COMMITTER_NAME" = "some name" ];
    then
    export GIT_COMMITTER_NAME="The Real Name";
    export GIT_COMMITTER_EMAIL="thereal@mail.com";
    fi
    if [ "$GIT_AUTHOR_NAME" = "some other name for same commiter" ];
    then
    export GIT_AUTHOR_NAME="The Real Name";
    export GIT_AUTHOR_EMAIL="thereal@mail.com";
    fi'
