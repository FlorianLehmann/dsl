grammar Arduinoml;

root                        :   declaration showStateMachine? bricks modes EOF;

declaration                 :   'application' name=IDENTIFIER;

showStateMachine            :   'SHOW STATE MACHINE';

bricks                      :   (sensor|actuator)+;
    sensor                  :   'sensor'   location debug?;
    actuator                :   'actuator' location debug?;
    location                :   identifier=IDENTIFIER ':' port=PORT_NUMBER;
    debug                   :   'DEBUG' debug_type=DEBUG_TYPE;

modes                       :   customMode* initialMode customMode*;
    initialMode             :   INITIAL customMode;
    customMode              :   identifier=IDENTIFIER '{' states modeTransition* '}';
    modeTransition          :   expression '=>' next_mode=IDENTIFIER;

states                      :   customState* initialState customState*;
    initialState            :   INITIAL customState;
    customState             :   identifier=IDENTIFIER '{'  action+ stateTransition* '}';
    action                  :   receiver=IDENTIFIER '<=' value=SIGNAL;
    stateTransition         :   expression '=>' next_state=IDENTIFIER;
    expression              :   expression operator=OPERATOR expression | comparison;
    comparison              :   analogicComparison | discreteComparison | temporalComparison;
    analogicComparison      :   trigger=IDENTIFIER operator=ANALOGIC_OPERATOR threshold=INTEGER;
    discreteComparison      :   trigger=IDENTIFIER 'IS' value=SIGNAL;
    temporalComparison      :   'AFTER' delay=INTEGER;



/*****************
 ** Lexer rules **
 *****************/

PORT_NUMBER                 :   [1-9] | '11' | '12';
IDENTIFIER                  :   LOWERCASE (LOWERCASE|UPPERCASE|NUMBER|UNDERSCORE)+;
SIGNAL                      :   'HIGH' | 'LOW';
INTEGER                     :   [1-9][0-9]*;
INITIAL                     :   '->';
OPERATOR                    :   'AND';
ANALOGIC_OPERATOR           :   '<' | '>';
DEBUG_TYPE                  :   'TEXT' | 'GRAPH';


/*************
 ** Helpers **
 *************/

fragment LOWERCASE          : [a-z];                                 // abstract rule, does not really exists
fragment UPPERCASE          : [A-Z];
fragment NUMBER             : [0-9];
fragment UNDERSCORE         : '_';
NEWLINE                     : ('\r'? '\n' | '\r')+      -> skip;
WS                          : ((' ' | '\t')+)           -> skip;     // who cares about whitespaces?
COMMENT                     : '#' ~( '\r' | '\n' )* -> skip; // Single line comments, starting with a #