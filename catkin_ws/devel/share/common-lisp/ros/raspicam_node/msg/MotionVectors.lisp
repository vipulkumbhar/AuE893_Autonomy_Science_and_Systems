; Auto-generated. Do not edit!


(cl:in-package raspicam_node-msg)


;//! \htmlinclude MotionVectors.msg.html

(cl:defclass <MotionVectors> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (mbx
    :reader mbx
    :initarg :mbx
    :type cl:fixnum
    :initform 0)
   (mby
    :reader mby
    :initarg :mby
    :type cl:fixnum
    :initform 0)
   (x
    :reader x
    :initarg :x
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 0 :element-type 'cl:fixnum :initial-element 0))
   (y
    :reader y
    :initarg :y
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 0 :element-type 'cl:fixnum :initial-element 0))
   (sad
    :reader sad
    :initarg :sad
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 0 :element-type 'cl:fixnum :initial-element 0)))
)

(cl:defclass MotionVectors (<MotionVectors>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MotionVectors>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MotionVectors)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name raspicam_node-msg:<MotionVectors> is deprecated: use raspicam_node-msg:MotionVectors instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <MotionVectors>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader raspicam_node-msg:header-val is deprecated.  Use raspicam_node-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'mbx-val :lambda-list '(m))
(cl:defmethod mbx-val ((m <MotionVectors>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader raspicam_node-msg:mbx-val is deprecated.  Use raspicam_node-msg:mbx instead.")
  (mbx m))

(cl:ensure-generic-function 'mby-val :lambda-list '(m))
(cl:defmethod mby-val ((m <MotionVectors>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader raspicam_node-msg:mby-val is deprecated.  Use raspicam_node-msg:mby instead.")
  (mby m))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <MotionVectors>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader raspicam_node-msg:x-val is deprecated.  Use raspicam_node-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <MotionVectors>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader raspicam_node-msg:y-val is deprecated.  Use raspicam_node-msg:y instead.")
  (y m))

(cl:ensure-generic-function 'sad-val :lambda-list '(m))
(cl:defmethod sad-val ((m <MotionVectors>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader raspicam_node-msg:sad-val is deprecated.  Use raspicam_node-msg:sad instead.")
  (sad m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MotionVectors>) ostream)
  "Serializes a message object of type '<MotionVectors>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mbx)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mby)) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    ))
   (cl:slot-value msg 'x))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    ))
   (cl:slot-value msg 'y))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'sad))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) ele) ostream))
   (cl:slot-value msg 'sad))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MotionVectors>) istream)
  "Deserializes a message object of type '<MotionVectors>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mbx)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mby)) (cl:read-byte istream))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'x) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'x)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256)))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'y) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'y)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256)))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'sad) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'sad)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:aref vals i)) (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MotionVectors>)))
  "Returns string type for a message object of type '<MotionVectors>"
  "raspicam_node/MotionVectors")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MotionVectors)))
  "Returns string type for a message object of type 'MotionVectors"
  "raspicam_node/MotionVectors")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MotionVectors>)))
  "Returns md5sum for a message object of type '<MotionVectors>"
  "f3b1d1ffbb5afc62c85d36a98f659ddf")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MotionVectors)))
  "Returns md5sum for a message object of type 'MotionVectors"
  "f3b1d1ffbb5afc62c85d36a98f659ddf")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MotionVectors>)))
  "Returns full string definition for message of type '<MotionVectors>"
  (cl:format cl:nil "# Message header~%std_msgs/Header header~%~%# Number of macroblocks in horizontal dimension~%uint8 mbx~%~%# Number of macroblocks in vertical dimension~%uint8 mby~%~%# Horizontal component of motion vectors~%int8[] x~%~%# Vertical component of motion vectors~%int8[] y~%~%# Sum of Absolute Difference metric of motion vectors~%uint16[] sad~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MotionVectors)))
  "Returns full string definition for message of type 'MotionVectors"
  (cl:format cl:nil "# Message header~%std_msgs/Header header~%~%# Number of macroblocks in horizontal dimension~%uint8 mbx~%~%# Number of macroblocks in vertical dimension~%uint8 mby~%~%# Horizontal component of motion vectors~%int8[] x~%~%# Vertical component of motion vectors~%int8[] y~%~%# Sum of Absolute Difference metric of motion vectors~%uint16[] sad~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MotionVectors>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     1
     1
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'x) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'y) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'sad) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 2)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MotionVectors>))
  "Converts a ROS message object to a list"
  (cl:list 'MotionVectors
    (cl:cons ':header (header msg))
    (cl:cons ':mbx (mbx msg))
    (cl:cons ':mby (mby msg))
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':sad (sad msg))
))
