#include <gtest/gtest.h>
#include "hello.h"

class HelloTest : public testing::Test
{
protected:
  HelloTest()
  {
  }

  virtual ~HelloTest()
  {
  }

  virtual void SetUp()
  {
  }

  virtual void TearDown()
  {
  }
};

TEST_F(HelloTest, ContainsHello)
{
  EXPECT_STREQ("Hello", hello());
}

int main(int argc, char *argv[])
{
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();  
}
