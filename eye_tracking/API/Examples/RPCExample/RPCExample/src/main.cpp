// Copyright (C) Smart Eye AB 2002-2023
// THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
// ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
// THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
// OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
// OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
// TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
// WITH THE CODE OR THE USE OR OTHER DEALINGS IN THE CODE.
//----------------------------------------------------------------------------//
// Smart Eye AB
// Första långgatan 28 B,
// 413 27 Göteborg, Sweden
// Contact: support@smarteye.se
//
// You are free to modify and use this code together with
// your purchased Smart Eye system.
//
// You MAY NOT distribute this code (modified or unmodified)
// without prior written consent from Smart Eye AB.
//----------------------------------------------------------------------------//

#include <iostream>
#include <sstream>
#include <map>
#include <functional>

#include "Simple.h"
#include "TrackAndRec.h"
#include "GetSetProfile.h"

int main(int argc, char* argv[])
{
  // Add new examples here
  std::map<std::string, std::function<int(void)>> examples = {
      {"Simple", Simple::run},
      {"TrackAndRec", TrackAndRec::run},
      {"GetSetProfile", GetSetProfile::run}};

  std::string validExamplesString;
  for (auto& example : examples)
  {
    validExamplesString.append(example.first);
    validExamplesString.append("\n");
  }

  std::stringstream usageDescription;
  usageDescription << "Usage: " << argv[0] << " Example\n\n"
                   << "Valid examples:\n"
                   << validExamplesString;

  if (argc < 2)
  {
    std::cerr << usageDescription.str() << std::endl;
    return 1;
  }

  std::string exampleName = argv[1];
  if (examples.find(exampleName) != examples.end())
  {
    return examples[exampleName]();
  }
  else
  {
    std::cerr << "Invalid example name.\n\n" << usageDescription.str();
    return 1;
  }
}
