package io.github.mosser.arduinoml.embedded.java.dsl;


import io.github.mosser.arduinoml.kernel.behavioral.SignalTransition;
import io.github.mosser.arduinoml.kernel.behavioral.State;
import io.github.mosser.arduinoml.kernel.behavioral.TimeTransition;
import io.github.mosser.arduinoml.kernel.behavioral.Transition;
import io.github.mosser.arduinoml.kernel.structural.SIGNAL;

import java.util.ArrayList;
import java.util.List;

public class TransitionBuilder {


    private TransitionTableBuilder parent;
    private Transition local;
    private String source;

    TransitionBuilder(TransitionTableBuilder parent, String source) {
        this.parent = parent;
        this.source = source;
    }

    public TransitionSignalBuilder when(String sensor) {
        SignalTransition signalTransition = new SignalTransition();
        this.local = signalTransition;
        parent.findState(source).addTransition(local);
        signalTransition.setSensor(parent.findSensor(sensor));
        return new TransitionSignalBuilder(this, signalTransition);
    }

    public TransitionBuilder after(long time) {
        TimeTransition timeTransition = new TimeTransition();
        this.local = timeTransition;
        parent.findState(source).addTransition(local);
        timeTransition.setTime(time);
        return this;
    }

    public TransitionTableBuilder goTo(String state) {
        this.local.setNext(parent.findState(state));
        return parent;
    }

}
