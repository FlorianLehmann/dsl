package io.github.mosser.arduinoml.embedded.java.dsl;

import io.github.mosser.arduinoml.kernel.behavioral.And;
import io.github.mosser.arduinoml.kernel.behavioral.SignalTransition;
import io.github.mosser.arduinoml.kernel.structural.SIGNAL;

public class TransitionAndBuilder {

    private TransitionBuilder transitionBuilder;
    private And local;

    public TransitionAndBuilder(TransitionBuilder transitionBuilder, And and) {
        this.local = and;
        this.transitionBuilder = transitionBuilder;
    }

    public TransitionBuilder hasStates(SIGNAL left, SIGNAL right) {
        local.setLeftValue(left);
        local.setRightValue(right);
        return transitionBuilder;
    }

}
