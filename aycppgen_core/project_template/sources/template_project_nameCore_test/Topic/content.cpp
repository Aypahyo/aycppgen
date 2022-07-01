#include <gtest/gtest.h>

#include <template_project_nameCore/Topic/content.hpp>

TEST(Content, ResultIsFour) {
  auto expected = 4;
  auto actual = core::topic::some();
  ASSERT_EQ(expected, actual);
}
