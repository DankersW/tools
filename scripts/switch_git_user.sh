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
                USER=$OPTARG
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

if [ -z "$USER" ]; then
    help Specify user
fi

echo "Setting git config to the $USER user"
if [ "$USER" == "work" ]; then
    git config --global user.email "wouter.dankers@vinnter.se"
    git config --global  user.name "Wouter Dankers"
    
elif [ "$USER" == "home" ]; then
    git config --global user.email "wouter.dankers@skynet.be"
    git config --global user.name "DankersW"
fi

echo "Git user name and email set to:"
git config --global user.email
git config --global user.name
