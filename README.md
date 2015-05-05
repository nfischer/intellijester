Intellijester
============
A joke telling application that interfaces with an Electro-Encephalogram to
tailor the jokes it tells you to your individual sense of humor. It uses the
EEG to detect which jokes you find funnier or less funny and uses machine
learning to judge which categories of jokes you prefer.

Installation
------------

### Python

You'll need to have the following python modules installed:

 - unirest
 - pyglet
 - qt4

The recommended installation method is to use the installation script.
Details of installation methods can be found within the script.

```Bash
$ sudo ./install.sh
```

### Audio

You will also need to install AVbin from
`https://avbin.github.io/AVbin/Download.html`

### Emotiv

You will need to download the control panel in order to interface with the
EEG. This can be found on `https://emotiv.com/store/product_72.html`

### Java

The parts of our project that interface with the EEG use Java.

To run the EEG files, you must have maven installed. You can download the
latest version here: `https://maven.apache.org/download.cgi`. Make sure to
export it to your path as well. You can verify this step by running the
command:

```Bash
$ mvn --version.
```

Then change to the eeg folder and install and run the application as follows:

```Bash
$ cd eeg/
$ mvn install
$ java -jar target/intelligester-1.0.jar
```
