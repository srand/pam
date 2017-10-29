#include "hello.h"

const char *hello()
{
#ifdef WINDOWS
  return "Hello Windows!";
#endif
#ifdef LINUX
  return "Hello Linux!";
#endif
#ifdef MACOSX
  return "Hello OSX!";
#endif
}
