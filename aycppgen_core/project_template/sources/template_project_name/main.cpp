#include <iostream>

#include <template_project_nameCore/Topic/content.hpp>
#include <template_project_nameAdapter/Topic/content.hpp>

int main(int argc, const char **argv) {
  /* construct and run the main application */
  std::cout << core::topic::some() << "\n";
  std::cout << adapter::topic::some() << std::endl;
  return 0;
}
