// Generated by gencpp from file sbg_driver/SbgAirData.msg
// DO NOT EDIT!


#ifndef SBG_DRIVER_MESSAGE_SBGAIRDATA_H
#define SBG_DRIVER_MESSAGE_SBGAIRDATA_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>
#include <sbg_driver/SbgAirDataStatus.h>

namespace sbg_driver
{
template <class ContainerAllocator>
struct SbgAirData_
{
  typedef SbgAirData_<ContainerAllocator> Type;

  SbgAirData_()
    : header()
    , time_stamp(0)
    , status()
    , pressure_abs(0.0)
    , altitude(0.0)
    , pressure_diff(0.0)
    , true_air_speed(0.0)
    , air_temperature(0.0)  {
    }
  SbgAirData_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , time_stamp(0)
    , status(_alloc)
    , pressure_abs(0.0)
    , altitude(0.0)
    , pressure_diff(0.0)
    , true_air_speed(0.0)
    , air_temperature(0.0)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef uint32_t _time_stamp_type;
  _time_stamp_type time_stamp;

   typedef  ::sbg_driver::SbgAirDataStatus_<ContainerAllocator>  _status_type;
  _status_type status;

   typedef double _pressure_abs_type;
  _pressure_abs_type pressure_abs;

   typedef double _altitude_type;
  _altitude_type altitude;

   typedef double _pressure_diff_type;
  _pressure_diff_type pressure_diff;

   typedef double _true_air_speed_type;
  _true_air_speed_type true_air_speed;

   typedef double _air_temperature_type;
  _air_temperature_type air_temperature;





  typedef boost::shared_ptr< ::sbg_driver::SbgAirData_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::sbg_driver::SbgAirData_<ContainerAllocator> const> ConstPtr;

}; // struct SbgAirData_

typedef ::sbg_driver::SbgAirData_<std::allocator<void> > SbgAirData;

typedef boost::shared_ptr< ::sbg_driver::SbgAirData > SbgAirDataPtr;
typedef boost::shared_ptr< ::sbg_driver::SbgAirData const> SbgAirDataConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::sbg_driver::SbgAirData_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::sbg_driver::SbgAirData_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace sbg_driver

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': True}
// {'geometry_msgs': ['/opt/ros/melodic/share/geometry_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg'], 'sbg_driver': ['/home/cambernard/workspaceUlysse/src/sbg_ros_driver/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::sbg_driver::SbgAirData_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::sbg_driver::SbgAirData_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::sbg_driver::SbgAirData_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::sbg_driver::SbgAirData_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::sbg_driver::SbgAirData_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::sbg_driver::SbgAirData_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::sbg_driver::SbgAirData_<ContainerAllocator> >
{
  static const char* value()
  {
    return "f7982abc9b7165b89ea4d8dda93717f9";
  }

  static const char* value(const ::sbg_driver::SbgAirData_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xf7982abc9b7165b8ULL;
  static const uint64_t static_value2 = 0x9ea4d8dda93717f9ULL;
};

template<class ContainerAllocator>
struct DataType< ::sbg_driver::SbgAirData_<ContainerAllocator> >
{
  static const char* value()
  {
    return "sbg_driver/SbgAirData";
  }

  static const char* value(const ::sbg_driver::SbgAirData_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::sbg_driver::SbgAirData_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# SBG Ellipse Messages\n"
"Header header\n"
"\n"
"# Time since sensor is powered up micro s\n"
"uint32 time_stamp\n"
"\n"
"# Airdata sensor status\n"
"SbgAirDataStatus status\n"
"\n"
"# Raw absolute pressure measured by the barometer sensor in Pascals.\n"
"float64 pressure_abs\n"
"\n"
"# Altitude computed from barometric altimeter in meters and positive upward.\n"
"float64 altitude\n"
"\n"
"# Raw differential pressure measured by the pitot tube in Pascal.\n"
"float64 pressure_diff\n"
"\n"
"# True airspeed measured by a pitot tube in m.s^-1 and positive forward.\n"
"float64 true_air_speed\n"
"\n"
"# Outside air temperature in °C that could be used to compute true airspeed from differential pressure.\n"
"float64 air_temperature\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
"\n"
"================================================================================\n"
"MSG: sbg_driver/SbgAirDataStatus\n"
"# SBG Ellipse Messages\n"
"# Submessage\n"
"\n"
"# True if the time stamp field represents a delay instead of an absolute time stamp.\n"
"bool is_delay_time\n"
"\n"
"# True if the pressure field is filled and valid.\n"
"bool pressure_valid\n"
"\n"
"# True if the barometric altitude field is filled and valid.\n"
"bool altitude_valid\n"
"\n"
"# True if the differential pressure field is filled and valid.\n"
"bool pressure_diff_valid\n"
"\n"
"# True if the true airspeed field is filled and valid.\n"
"bool air_speed_valid\n"
"\n"
"# True if the output air temperature field is filled and valid.\n"
"bool air_temperature_valid\n"
;
  }

  static const char* value(const ::sbg_driver::SbgAirData_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::sbg_driver::SbgAirData_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.time_stamp);
      stream.next(m.status);
      stream.next(m.pressure_abs);
      stream.next(m.altitude);
      stream.next(m.pressure_diff);
      stream.next(m.true_air_speed);
      stream.next(m.air_temperature);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct SbgAirData_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::sbg_driver::SbgAirData_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::sbg_driver::SbgAirData_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "time_stamp: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.time_stamp);
    s << indent << "status: ";
    s << std::endl;
    Printer< ::sbg_driver::SbgAirDataStatus_<ContainerAllocator> >::stream(s, indent + "  ", v.status);
    s << indent << "pressure_abs: ";
    Printer<double>::stream(s, indent + "  ", v.pressure_abs);
    s << indent << "altitude: ";
    Printer<double>::stream(s, indent + "  ", v.altitude);
    s << indent << "pressure_diff: ";
    Printer<double>::stream(s, indent + "  ", v.pressure_diff);
    s << indent << "true_air_speed: ";
    Printer<double>::stream(s, indent + "  ", v.true_air_speed);
    s << indent << "air_temperature: ";
    Printer<double>::stream(s, indent + "  ", v.air_temperature);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SBG_DRIVER_MESSAGE_SBGAIRDATA_H