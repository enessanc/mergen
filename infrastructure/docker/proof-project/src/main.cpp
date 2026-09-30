#include <cstdlib>
#include <iostream>
#include <string_view>

int main() {
  const char* requested_failure = std::getenv("MERGEN_PROOF_FAIL");
  if (requested_failure != nullptr && std::string_view(requested_failure) == "1") {
    std::cerr << "Intentional Mergen runtime proof failure\n";
    return 1;
  }

  std::cout << "Mergen C++/CMake runtime proof passed\n";
  return 0;
}
