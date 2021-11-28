// Generated by gencpp from file model_server/ImageRequestResponse.msg
// DO NOT EDIT!


#ifndef MODEL_SERVER_MESSAGE_IMAGEREQUESTRESPONSE_H
#define MODEL_SERVER_MESSAGE_IMAGEREQUESTRESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Bool.h>

namespace model_server
{
template <class ContainerAllocator>
struct ImageRequestResponse_
{
  typedef ImageRequestResponse_<ContainerAllocator> Type;

  ImageRequestResponse_()
    : status()  {
    }
  ImageRequestResponse_(const ContainerAllocator& _alloc)
    : status(_alloc)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Bool_<ContainerAllocator>  _status_type;
  _status_type status;





  typedef boost::shared_ptr< ::model_server::ImageRequestResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::model_server::ImageRequestResponse_<ContainerAllocator> const> ConstPtr;

}; // struct ImageRequestResponse_

typedef ::model_server::ImageRequestResponse_<std::allocator<void> > ImageRequestResponse;

typedef boost::shared_ptr< ::model_server::ImageRequestResponse > ImageRequestResponsePtr;
typedef boost::shared_ptr< ::model_server::ImageRequestResponse const> ImageRequestResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::model_server::ImageRequestResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::model_server::ImageRequestResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::model_server::ImageRequestResponse_<ContainerAllocator1> & lhs, const ::model_server::ImageRequestResponse_<ContainerAllocator2> & rhs)
{
  return lhs.status == rhs.status;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::model_server::ImageRequestResponse_<ContainerAllocator1> & lhs, const ::model_server::ImageRequestResponse_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace model_server

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::model_server::ImageRequestResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::model_server::ImageRequestResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::model_server::ImageRequestResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::model_server::ImageRequestResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::model_server::ImageRequestResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::model_server::ImageRequestResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::model_server::ImageRequestResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "17b637004ab60f377423869fa9425b3c";
  }

  static const char* value(const ::model_server::ImageRequestResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x17b637004ab60f37ULL;
  static const uint64_t static_value2 = 0x7423869fa9425b3cULL;
};

template<class ContainerAllocator>
struct DataType< ::model_server::ImageRequestResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "model_server/ImageRequestResponse";
  }

  static const char* value(const ::model_server::ImageRequestResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::model_server::ImageRequestResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "std_msgs/Bool   status\n"
"\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Bool\n"
"bool data\n"
;
  }

  static const char* value(const ::model_server::ImageRequestResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::model_server::ImageRequestResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.status);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct ImageRequestResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::model_server::ImageRequestResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::model_server::ImageRequestResponse_<ContainerAllocator>& v)
  {
    s << indent << "status: ";
    s << std::endl;
    Printer< ::std_msgs::Bool_<ContainerAllocator> >::stream(s, indent + "  ", v.status);
  }
};

} // namespace message_operations
} // namespace ros

#endif // MODEL_SERVER_MESSAGE_IMAGEREQUESTRESPONSE_H
