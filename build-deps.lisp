#|
(handler-bind ((conditions:stack-overflow
                #'(lambda (c)
                    (and (< (current-stack-length) 50000)
                         (continue)))))
  (progn
    (asdf:operate 'asdf:monolithic-concatenate-source-op 'bordeaux-threads)
    (asdf:operate 'asdf:monolithic-concatenate-source-op 'jsown)
    (asdf:operate 'asdf:monolithic-concatenate-source-op 'usocket)))
|#

;(load "/Users/ryanhope/quicklisp/asdf.lisp")

(asdf:defsystem :jni 
  :depends-on (bordeaux-threads usocket jsown)
  :components ((:file "json-network-interface")))


(asdf:operate (make-instance 'asdf::monolithic-concatenate-source-op) (asdf:find-system :jni)))
