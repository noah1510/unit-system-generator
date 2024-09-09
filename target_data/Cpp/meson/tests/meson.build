#make both dependencies into one array
gtest_dep = dependency('gtest', required: true, fallback:['gtest','gtest_dep'])

tests_17 = [
    'unit_test_17',
    'base_units_test_17',
    'common_test_17',
]

tests = [
    'unit_test',
    'base_units_test',
    'common_test',
]

test_incdir = include_directories('.')

#create all the tests
foreach test_obj : tests_17
    deps = [
        dependency('unit-system', required: true),
        gtest_dep,
    ]
    exe = executable(
        test_obj, 
        test_obj + '.cpp',
        dependencies: deps,
        include_directories : test_incdir,
    )
    test(
        test_obj + ' Test',
        exe,
        protocol: 'gtest',
    )
endforeach
