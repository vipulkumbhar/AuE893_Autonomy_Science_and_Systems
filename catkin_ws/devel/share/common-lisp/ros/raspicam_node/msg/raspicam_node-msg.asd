
(cl:in-package :asdf)

(defsystem "raspicam_node-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "MotionVectors" :depends-on ("_package_MotionVectors"))
    (:file "_package_MotionVectors" :depends-on ("_package"))
  ))