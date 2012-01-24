#include <python3.1/Python.h>

int main() {
  Py_Initialize();
  PyRun_SimpleString("print('brave sir robin')");
}
