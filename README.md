# Installation

## From Source

Copy the [json-network-interface.lisp](json-network-interface.lisp) file to ```modules``` subfolder of your ACT-R installation.

#### Common Lisp Dependencies

* jsown
* bordeaux-threads
* usocket

These libraries can be installed with [quicklisp](http://www.quicklisp.org/beta):

```lisp
(ql:quickload '("jsown" "bordeaux-threads" "usocket"))
```

## From Binaries

Download this archive: http://ompldr.org/vaTFmeA/json-network-interface-darwin-04092013.zip

#### For The Source Based ACT-R

Extract the above archive into the user-loads directory.

#### For The Standalone Version of ACT-R

Extract the above archive into the patches directory.
