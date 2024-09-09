#make both dependencies into one array
gtest_dep = dependency('gtest', required: true, fallback:['gtest','gtest_dep'])

tests_17 = [
    'unit_test_17',
    'base_units_test_17',
    'common_test_17',
]

tests_20 = [
    'unit_test_20',
    'base_units_test_20',
    'common_test_20',
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

foreach test_obj : tests_20
    deps = [
        dependency('unit-system-20', required: true),
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
