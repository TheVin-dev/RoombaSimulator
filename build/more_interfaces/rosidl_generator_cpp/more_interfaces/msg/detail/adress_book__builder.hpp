// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from more_interfaces:msg/AdressBook.idl
// generated code does not contain a copyright notice

#ifndef MORE_INTERFACES__MSG__DETAIL__ADRESS_BOOK__BUILDER_HPP_
#define MORE_INTERFACES__MSG__DETAIL__ADRESS_BOOK__BUILDER_HPP_

#include "more_interfaces/msg/detail/adress_book__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace more_interfaces
{

namespace msg
{

namespace builder
{

class Init_AdressBook_adress
{
public:
  explicit Init_AdressBook_adress(::more_interfaces::msg::AdressBook & msg)
  : msg_(msg)
  {}
  ::more_interfaces::msg::AdressBook adress(::more_interfaces::msg::AdressBook::_adress_type arg)
  {
    msg_.adress = std::move(arg);
    return std::move(msg_);
  }

private:
  ::more_interfaces::msg::AdressBook msg_;
};

class Init_AdressBook_age
{
public:
  explicit Init_AdressBook_age(::more_interfaces::msg::AdressBook & msg)
  : msg_(msg)
  {}
  Init_AdressBook_adress age(::more_interfaces::msg::AdressBook::_age_type arg)
  {
    msg_.age = std::move(arg);
    return Init_AdressBook_adress(msg_);
  }

private:
  ::more_interfaces::msg::AdressBook msg_;
};

class Init_AdressBook_gender
{
public:
  explicit Init_AdressBook_gender(::more_interfaces::msg::AdressBook & msg)
  : msg_(msg)
  {}
  Init_AdressBook_age gender(::more_interfaces::msg::AdressBook::_gender_type arg)
  {
    msg_.gender = std::move(arg);
    return Init_AdressBook_age(msg_);
  }

private:
  ::more_interfaces::msg::AdressBook msg_;
};

class Init_AdressBook_last_name
{
public:
  explicit Init_AdressBook_last_name(::more_interfaces::msg::AdressBook & msg)
  : msg_(msg)
  {}
  Init_AdressBook_gender last_name(::more_interfaces::msg::AdressBook::_last_name_type arg)
  {
    msg_.last_name = std::move(arg);
    return Init_AdressBook_gender(msg_);
  }

private:
  ::more_interfaces::msg::AdressBook msg_;
};

class Init_AdressBook_first_name
{
public:
  Init_AdressBook_first_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AdressBook_last_name first_name(::more_interfaces::msg::AdressBook::_first_name_type arg)
  {
    msg_.first_name = std::move(arg);
    return Init_AdressBook_last_name(msg_);
  }

private:
  ::more_interfaces::msg::AdressBook msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::more_interfaces::msg::AdressBook>()
{
  return more_interfaces::msg::builder::Init_AdressBook_first_name();
}

}  // namespace more_interfaces

#endif  // MORE_INTERFACES__MSG__DETAIL__ADRESS_BOOK__BUILDER_HPP_
