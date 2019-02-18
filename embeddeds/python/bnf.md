<syntax> ::= <declaration> <showStateMachine> <bricks> <modes>

<declaration> ::= application <identifier>

<showStateMachine> ::= SHOW STATE MACHINE

<modes> ::= <initialMode> { <mode> }
<initialMode> ::= -> <mode>
<mode> ::= <identifier> "{" <states> { <transition> } "}"

<bricks> ::= { <sensor> | <actuator> }
<sensor> ::= sensor <location> <debug>
<actuator> ::= actuator <location> [<debug>]
<location> ::= <identifier> : <portNumber>
<debug> ::= DEBUG (TEXT | GRAPH)

<states> ::= <initialState> { <state> }
<initialState> ::= -> <state>
<state> ::= <identifier> "{" <action>+ { <transition> } "}"
<action> ::= <identifier> <= <signal>
<transition> ::= <expression> => <identifier>

<expression> ::= (<expression><operator><expression> | <comparison>)
<operator> ::= AND
<identifier> ::= letter { letter | digit | _ }
<comparison> ::= (<analogicComparison>| <discreteComparison> | <temporalComparison>)
<discreteComparison> ::= <identifier> is <signal>
<analogicComparison> ::= <identifier> (< | >) <digit>+
<temporalComparison> ::= after <digit>+

<signal> ::= HIGH | LOW
<digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<letter> ::= a | b | c | ... | y | z
<portNumber> ::= digit | 10 | 11 | 12