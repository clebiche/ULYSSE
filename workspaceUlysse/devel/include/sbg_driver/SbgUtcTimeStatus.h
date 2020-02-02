// Generated by gencpp from file sbg_driver/SbgUtcTimeStatus.msg
// DO NOT EDIT!


#ifndef SBG_DRIVER_MESSAGE_SBGUTCTIMESTATUS_H
#define SBG_DRIVER_MESSAGE_SBGUTCTIMESTATUS_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace sbg_driver
{
template <class ContainerAllocator>
struct SbgUtcTimeStatus_
{
  typedef SbgUtcTimeStatus_<ContainerAllocator> Type;

  SbgUtcTimeStatus_()
    : clock_stable(false)
    , clock_status(0)
    , clock_utc_sync(false)
    , clock_utc_status(0)  {
    }
  SbgUtcTimeStatus_(const ContainerAllocator& _alloc)
    : clock_stable(false)
    , clock_status(0)
    , clock_utc_sync(false)
    , clock_utc_status(0)  {
  (void)_alloc;
    }



   typedef uint8_t _clock_stable_type;
  _clock_stable_type clock_stable;

   typedef uint8_t _clock_status_type;
  _clock_status_type clock_status;

   typedef uint8_t _clock_utc_sync_type;
  _clock_utc_sync_type clock_utc_sync;

   typedef uint8_t _clock_utc_status_type;
  _clock_utc_status_type clock_utc_status;





  typedef boost::shared_ptr< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> const> ConstPtr;

}; // struct SbgUtcTimeStatus_

typedef ::sbg_driver::SbgUtcTimeStatus_<std::allocator<void> > SbgUtcTimeStatus;

typedef boost::shared_ptr< ::sbg_driver::SbgUtcTimeStatus > SbgUtcTimeStatusPtr;
typedef boost::shared_ptr< ::sbg_driver::SbgUtcTimeStatus const> SbgUtcTimeStatusConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace sbg_driver

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'geometry_msgs': ['/opt/ros/melodic/share/geometry_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg'], 'sbg_driver': ['/home/cambernard/workspaceUlysse/src/sbg_ros_driver/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d140f95192866cb459fe7af2851c8eed";
  }

  static const char* value(const ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd140f95192866cb4ULL;
  static const uint64_t static_value2 = 0x59fe7af2851c8eedULL;
};

template<class ContainerAllocator>
struct DataType< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> >
{
  static const char* value()
  {
    return "sbg_driver/SbgUtcTimeStatus";
  }

  static const char* value(const ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# SBG Ellipse Messages\n"
"\n"
"# True when a clock input can be used to synchronize the internal clock.\n"
"bool clock_stable\n"
"\n"
"# Define the internal clock estimation status\n"
"# 0 An error has occurred on the clock estimation.\n"
"# 1 The clock is only based on the internal crystal.\n"
"# 2 A PPS has been detected and the clock is converging to it.\n"
"# 3 The clock has converged to the PPS and is within 500ns.\n"
"uint8 clock_status\n"
"\n"
"# True if UTC time is synchronized with a PPS\n"
"bool clock_utc_sync\n"
"\n"
"# UTC validity status\n"
"# 0 The UTC time is not known, we are just propagating the UTC time internally.\n"
"# 1 We have received valid UTC time information but we don't have the leap seconds information.\n"
"# 2 We have received valid UTC time data with valid leap seconds.\n"
"uint8 clock_utc_status\n"
;
  }

  static const char* value(const ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.clock_stable);
      stream.next(m.clock_status);
      stream.next(m.clock_utc_sync);
      stream.next(m.clock_utc_status);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct SbgUtcTimeStatus_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::sbg_driver::SbgUtcTimeStatus_<ContainerAllocator>& v)
  {
    s << indent << "clock_stable: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.clock_stable);
    s << indent << "clock_status: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.clock_status);
    s << indent << "clock_utc_sync: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.clock_utc_sync);
    s << indent << "clock_utc_status: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.clock_utc_status);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SBG_DRIVER_MESSAGE_SBGUTCTIMESTATUS_H