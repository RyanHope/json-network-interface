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
