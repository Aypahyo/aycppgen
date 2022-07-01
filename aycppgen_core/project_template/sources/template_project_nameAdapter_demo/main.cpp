
#include <map>
#include <functional>
#include <iostream>

#include <template_project_nameAdapter_demo/Foo/Foo.hpp>

void insertAllOptions(std::map<std::string, std::function<void()>> &map);

int main([[maybe_unused]] int argc, [[maybe_unused]] char **argv) {
  /*manual exploratory things that are hard to unit test*/
  auto demos = std::map<std::string, std::function<void()>>();
  insertAllOptions(demos);
  std::string selection;
  for (const auto &kvp : demos) {
    std::cout << kvp.first << " ";
  }
  std::cout << "\nSelection: ";
  std::cin >> selection;
  std::cout << "Starting: " << selection << "\n";
  demos[selection]();
  std::cout << "\nDone: " << selection << std::endl;
  return 0;
}

void insertAllOptions(std::map<std::string, std::function<void()>> &map) {
  map.insert_or_assign("nothing", []() { std::cout << "taddaaaa"; });
  map.insert_or_assign("foo", []() { Foo().Run(); });
}