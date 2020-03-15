;; Auto-generated. Do not edit!


(when (boundp 'raspicam_node::MotionVectors)
  (if (not (find-package "RASPICAM_NODE"))
    (make-package "RASPICAM_NODE"))
  (shadow 'MotionVectors (find-package "RASPICAM_NODE")))
(unless (find-package "RASPICAM_NODE::MOTIONVECTORS")
  (make-package "RASPICAM_NODE::MOTIONVECTORS"))

(in-package "ROS")
;;//! \htmlinclude MotionVectors.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass raspicam_node::MotionVectors
  :super ros::object
  :slots (_header _mbx _mby _x _y _sad ))

(defmethod raspicam_node::MotionVectors
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:mbx __mbx) 0)
    ((:mby __mby) 0)
    ((:x __x) (make-array 0 :initial-element 0 :element-type :integer))
    ((:y __y) (make-array 0 :initial-element 0 :element-type :integer))
    ((:sad __sad) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _header __header)
   (setq _mbx (round __mbx))
   (setq _mby (round __mby))
   (setq _x __x)
   (setq _y __y)
   (setq _sad __sad)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:mbx
   (&optional __mbx)
   (if __mbx (setq _mbx __mbx)) _mbx)
  (:mby
   (&optional __mby)
   (if __mby (setq _mby __mby)) _mby)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:sad
   (&optional __sad)
   (if __sad (setq _sad __sad)) _sad)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; uint8 _mbx
    1
    ;; uint8 _mby
    1
    ;; int8[] _x
    (* 1    (length _x)) 4
    ;; int8[] _y
    (* 1    (length _y)) 4
    ;; uint16[] _sad
    (* 2    (length _sad)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; uint8 _mbx
       (write-byte _mbx s)
     ;; uint8 _mby
       (write-byte _mby s)
     ;; int8[] _x
     (write-long (length _x) s)
     (dotimes (i (length _x))
       (write-byte (elt _x i) s)
       )
     ;; int8[] _y
     (write-long (length _y) s)
     (dotimes (i (length _y))
       (write-byte (elt _y i) s)
       )
     ;; uint16[] _sad
     (write-long (length _sad) s)
     (dotimes (i (length _sad))
       (write-word (elt _sad i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; uint8 _mbx
     (setq _mbx (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _mby
     (setq _mby (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; int8[] _x
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _x (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _x i) (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> (elt _x i) 127) (setf (elt _x i) (- (elt _x i) 256)))
     ))
   ;; int8[] _y
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _y (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _y i) (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> (elt _y i) 127) (setf (elt _y i) (- (elt _y i) 256)))
     ))
   ;; uint16[] _sad
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _sad (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _sad i) (sys::peek buf ptr- :short)) (incf ptr- 2)
     ))
   ;;
   self)
  )

(setf (get raspicam_node::MotionVectors :md5sum-) "f3b1d1ffbb5afc62c85d36a98f659ddf")
(setf (get raspicam_node::MotionVectors :datatype-) "raspicam_node/MotionVectors")
(setf (get raspicam_node::MotionVectors :definition-)
      "# Message header
std_msgs/Header header

# Number of macroblocks in horizontal dimension
uint8 mbx

# Number of macroblocks in vertical dimension
uint8 mby

# Horizontal component of motion vectors
int8[] x

# Vertical component of motion vectors
int8[] y

# Sum of Absolute Difference metric of motion vectors
uint16[] sad

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

")



(provide :raspicam_node/MotionVectors "f3b1d1ffbb5afc62c85d36a98f659ddf")


