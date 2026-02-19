PA3

Two categories of tests: 
10 tests which should parse successfully (testpass0.ac through testpass9.ac)
10 tests which should fail to parse (testfail0.ac through testfail9.ac)

The 10 fail cases are:
•	testfail0.ac: trailing operator (a=6+)
•	testfail1.ac: leading operator (a=+6)
•	testfail2.ac: missing right parenthesis (a=6*(b+7)
•	testfail3.ac: extra right parenthesis (a=6*b)+7)
•	testfail4.ac: missing operand before ) (a=(6+))
•	testfail5.ac: missing operator between operands (a=6 7+8)
•	testfail6.ac: operator immediately after ( (a=6*(+7))
•	testfail7.ac: “extra tokens after statement” (ia=5)
•	testfail8.ac: empty parentheses-ish (a=( ))
•	testfail9.ac: two operators in a row (a=2^^3)