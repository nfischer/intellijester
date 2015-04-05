Intellijester
=============

A joke telling application that interfaces with an Electro-Encephalogram to
tailor the jokes it tells you to your individual sense of humor. It uses the
EEG to detect which jokes you find funnier or less funny and uses machine
learning to judge which categories of jokes you prefer.

Installation
------------

You'll need to have the following python modules installed:

 - unirest
 - gi

You can install these with pip as follows:

```Bash
$ sudo pip install unirest
$ sudo pip install gi
```

If you need to install pip, try these steps:

```Bash
# Linux
$ sudo apt-get install python-pip

# Mac
$ sudo easy_install pip
```

To run the EEG files, you must have maven installed. You can download it here: https://maven.apache.org/download.cgi. Make sure to export it to your path as well. You can verify this step by typing mvn --version.

Navigate into the ee branch and install and run using these steps:

```Bash
$ mvn install
$ java -jar target/intelligester-1.0.jar
```
