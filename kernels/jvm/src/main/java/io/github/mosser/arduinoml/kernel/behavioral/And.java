package io.github.mosser.arduinoml.kernel.behavioral;

import io.github.mosser.arduinoml.kernel.generator.Visitor;
import io.github.mosser.arduinoml.kernel.structural.SIGNAL;
import io.github.mosser.arduinoml.kernel.structural.Sensor;

public class And extends Transition {
    private Sensor leftSensor;
    private SIGNAL leftValue;
    private Sensor rightSensor;
    private SIGNAL rightValue;

    public Sensor getLeftSensor() {
        return leftSensor;
    }

    public void setLeftSensor(Sensor leftSensor) {
        this.leftSensor = leftSensor;
    }

    public SIGNAL getLeftValue() {
        return leftValue;
    }

    public void setLeftValue(SIGNAL leftValue) {
        this.leftValue = leftValue;
    }

    public Sensor getRightSensor() {
        return rightSensor;
    }

    public void setRightSensor(Sensor rightSensor) {
        this.rightSensor = rightSensor;
    }

    public SIGNAL getRightValue() {
        return rightValue;
    }

    public void setRightValue(SIGNAL rightValue) {
        this.rightValue = rightValue;
    }

    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}
