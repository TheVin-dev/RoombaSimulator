// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from more_interfaces:msg/AdressBook.idl
// generated code does not contain a copyright notice

#ifndef MORE_INTERFACES__MSG__DETAIL__ADRESS_BOOK__STRUCT_H_
#define MORE_INTERFACES__MSG__DETAIL__ADRESS_BOOK__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'FEMALE'.
static const bool more_interfaces__msg__AdressBook__FEMALE = true;

/// Constant 'MALE'.
static const bool more_interfaces__msg__AdressBook__MALE = false;

// Include directives for member types
// Member 'first_name'
// Member 'last_name'
// Member 'adress'
#include "rosidl_runtime_c/string.h"

// Struct defined in msg/AdressBook in the package more_interfaces.
typedef struct more_interfaces__msg__AdressBook
{
  rosidl_runtime_c__String first_name;
  rosidl_runtime_c__String last_name;
  bool gender;
  uint8_t age;
  rosidl_runtime_c__String adress;
} more_interfaces__msg__AdressBook;

// Struct for a sequence of more_interfaces__msg__AdressBook.
typedef struct more_interfaces__msg__AdressBook__Sequence
{
  more_interfaces__msg__AdressBook * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} more_interfaces__msg__AdressBook__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MORE_INTERFACES__MSG__DETAIL__ADRESS_BOOK__STRUCT_H_
