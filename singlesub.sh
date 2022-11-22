#! /usr/bin/sh
read -p "Enter student name:" name
read -p "Enter Student Repo Link:" link
cd "singleSubFile"
mkdir ${name}
cd ${name}
git clone ${link} .
rspec
echo "done"
