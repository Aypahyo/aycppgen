#include "Foo.hpp"
#include <iostream>
#include <template_project_nameAdapter/Topic/content.hpp>

void Foo::Run() {
  std::cout << adapter::topic::some() << std::endl;
}