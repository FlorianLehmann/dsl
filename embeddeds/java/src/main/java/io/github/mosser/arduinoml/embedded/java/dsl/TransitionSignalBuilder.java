package io.github.mosser.arduinoml.embedded.java.dsl;

import io.github.mosser.arduinoml.kernel.behavioral.SignalTransition;
import io.github.mosser.arduinoml.kernel.structural.SIGNAL;

public class TransitionSignalBuilder {

    private TransitionBuilder transitionBuilder;
    private SignalTransition local;

    public TransitionSignalBuilder(TransitionBuilder transitionBuilder, SignalTransition signalTransition) {
        this.local = signalTransition;
        this.transitionBuilder = transitionBuilder;
    }

    public TransitionBuilder isHigh() {
        local.setValue(SIGNAL.HIGH);
        return transitionBuilder;
    }

    public TransitionBuilder isLow() {
        local.setValue(SIGNAL.LOW);
        return transitionBuilder;
    }

}
