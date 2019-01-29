grammar Arduinoml;


/******************
 ** Parser rules **
 ******************/

root                        :   declaration bricks states EOF;

declaration                 :   'application' name=IDENTIFIER;

bricks                      :   (sensor|actuator)+;
    sensor                  :   'sensor'   location ;
    actuator                :   'actuator' location ;
    location                :   id=IDENTIFIER ':' port=PORT_NUMBER;

states                      :   state+;
    state                   :   initial? name=IDENTIFIER '{'  action+ transition+ '}';
    action                  :   receiver=IDENTIFIER '<=' value=SIGNAL;
    transition              :   (signal_transition | temporal_transition | and_transition);
    signal_transition       :   trigger=IDENTIFIER 'is' value=SIGNAL '=>' next=IDENTIFIER;
    temporal_transition     :   'after' delay=DELAY '=>' next=IDENTIFIER;
    and_transition          :   left_trigger=IDENTIFIER 'is' left_value=SIGNAL 'and' right_trigger=IDENTIFIER 'is' right_value=SIGNAL '=>' next=IDENTIFIER;
    initial                 :   '->';

/*****************
 ** Lexer rules **
 *****************/

PORT_NUMBER                 :   [1-9] | '11' | '12';
IDENTIFIER                  :   LOWERCASE (LOWERCASE|UPPERCASE|NUMBER|UNDERSCORE)+;
SIGNAL                      :   'HIGH' | 'LOW';
DELAY                       :   [1-9][0-9]*;

/*************
 ** Helpers **
 *************/

fragment LOWERCASE          : [a-z];                                 // abstract rule, does not really exists
fragment UPPERCASE          : [A-Z];
fragment NUMBER             : [0-9];
fragment UNDERSCORE         : '_';
NEWLINE                     : ('\r'? '\n' | '\r')+      -> skip;
WS                          : ((' ' | '\t')+)           -> skip;     // who cares about whitespaces?
COMMENT                     : '#' ~( '\r' | '\n' )*     -> skip;     // Single line comments, starting with a #
