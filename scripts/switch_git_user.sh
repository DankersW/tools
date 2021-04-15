#!/bin/bash

help() {
    echo "FAIL: $@"
    echo "Usage: $0 -u [work | home] " 1>&2
    exit 1
}

while getopts "u:" opt; do
    case "${opt}" in
        u)
            if [ "$OPTARG" == "work" ] || [ "$OPTARG" == "home" ]; then
               	GIT_USER=$OPTARG
            else
                help unsupported user $OPTARG
            fi
            ;;
        *)
            help illegal option "$OPTARG"
            ;;
    esac
done
shift $((OPTIND -1))

if [ -z "$GIT_USER" ]; then
    help Specify git user
fi

echo "Setting git config to the $GIT_USER user"
if [ "$GIT_USER" == "work" ]; then
    git config --global user.email "wouter.dankers@vinnter.se"
    git config --global  user.name "Wouter Dankers"
    
elif [ "$GIT_USER" == "home" ]; then
    git config --global user.email "wouter.dankers@skynet.be"
    git config --global user.name "DankersW"
fi

echo "Git user name and email set to:"
git config --global user.email
git config --global user.name
