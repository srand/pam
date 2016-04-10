

int test_cxx_source();
int test_cxx_source_regex();
int test_cxx_source_tool();

int main()
{
    int rv = 0;
    
    rv += test_cxx_source();
    rv += test_cxx_source_regex();
    rv += test_cxx_source_tool();
    
    return 0;
}
