<expression> ::= (<expression><operator><expression> | <comparison>)
<operator> ::= AND
<identifier> ::= letter { letter | digit | _ }
<comparison> ::= (<analogicComparison>| <discreteComparison> | <temporalComparison>)
<discreteComparison> ::= <identifier> is <signal>
<analogicComparison> ::= <identifier> (< | >) <digit>+
<temporalComparison> ::=  <digit>+ >  <digit>+

<signal> ::= HIGH | LOW
<digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<letter> ::= a | b | c | ... | y | z