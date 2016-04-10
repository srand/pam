int test_cxx_dep();
int test_cxx_dep_transitive();

int main()
{
    return test_cxx_dep() + test_cxx_dep_transitive();
}
