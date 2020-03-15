// Auto-generated. Do not edit!

// (in-package raspicam_node.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class MotionVectors {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.mbx = null;
      this.mby = null;
      this.x = null;
      this.y = null;
      this.sad = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('mbx')) {
        this.mbx = initObj.mbx
      }
      else {
        this.mbx = 0;
      }
      if (initObj.hasOwnProperty('mby')) {
        this.mby = initObj.mby
      }
      else {
        this.mby = 0;
      }
      if (initObj.hasOwnProperty('x')) {
        this.x = initObj.x
      }
      else {
        this.x = [];
      }
      if (initObj.hasOwnProperty('y')) {
        this.y = initObj.y
      }
      else {
        this.y = [];
      }
      if (initObj.hasOwnProperty('sad')) {
        this.sad = initObj.sad
      }
      else {
        this.sad = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MotionVectors
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [mbx]
    bufferOffset = _serializer.uint8(obj.mbx, buffer, bufferOffset);
    // Serialize message field [mby]
    bufferOffset = _serializer.uint8(obj.mby, buffer, bufferOffset);
    // Serialize message field [x]
    bufferOffset = _arraySerializer.int8(obj.x, buffer, bufferOffset, null);
    // Serialize message field [y]
    bufferOffset = _arraySerializer.int8(obj.y, buffer, bufferOffset, null);
    // Serialize message field [sad]
    bufferOffset = _arraySerializer.uint16(obj.sad, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MotionVectors
    let len;
    let data = new MotionVectors(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [mbx]
    data.mbx = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [mby]
    data.mby = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [x]
    data.x = _arrayDeserializer.int8(buffer, bufferOffset, null)
    // Deserialize message field [y]
    data.y = _arrayDeserializer.int8(buffer, bufferOffset, null)
    // Deserialize message field [sad]
    data.sad = _arrayDeserializer.uint16(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += object.x.length;
    length += object.y.length;
    length += 2 * object.sad.length;
    return length + 14;
  }

  static datatype() {
    // Returns string type for a message object
    return 'raspicam_node/MotionVectors';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f3b1d1ffbb5afc62c85d36a98f659ddf';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # Message header
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new MotionVectors(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.mbx !== undefined) {
      resolved.mbx = msg.mbx;
    }
    else {
      resolved.mbx = 0
    }

    if (msg.mby !== undefined) {
      resolved.mby = msg.mby;
    }
    else {
      resolved.mby = 0
    }

    if (msg.x !== undefined) {
      resolved.x = msg.x;
    }
    else {
      resolved.x = []
    }

    if (msg.y !== undefined) {
      resolved.y = msg.y;
    }
    else {
      resolved.y = []
    }

    if (msg.sad !== undefined) {
      resolved.sad = msg.sad;
    }
    else {
      resolved.sad = []
    }

    return resolved;
    }
};

module.exports = MotionVectors;
