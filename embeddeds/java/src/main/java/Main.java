import io.github.mosser.arduinoml.kernel.App;
import io.github.mosser.arduinoml.kernel.generator.ToWiring;
import io.github.mosser.arduinoml.kernel.generator.Visitor;

import static io.github.mosser.arduinoml.embedded.java.dsl.AppBuilder.*;

public class Main {


    public static void main (String[] args) {

        // SCENARIO 1
        /*App myApp =
                application("red_button")
                        .uses(sensor("button", 9))
                        .uses(actuator("led", 12))
                        .uses(actuator("buzzer", 11))
                        .hasForState("initial").initial()
                            .setting("led").toLow()
                            .setting("buzzer").toLow()
                        .endState()
                        .hasForState("ledAndBuzzer")
                            .setting("led").toHigh()
                            .setting("buzzer").toHigh()
                        .endState()
                        .beginTransitionTable()
                            .from("initial").when("button").isHigh().goTo("ledAndBuzzer")
                            .from("ledAndBuzzer").when("button").isLow().goTo("initial")
                        .endTransitionTable()
                .build();*/

        // SCENARIO 2
        /*App myApp =
                application("red_button")
                        .uses(sensor("button1", 9))
                        .uses(sensor("button2", 10))
                        .uses(actuator("led", 12))
                        .hasForState("initial").initial()
                            .setting("led").toLow()
                        .endState()
                        .hasForState("button1")
                            .setting("led").toLow()
                        .endState()
                        .hasForState("button2")
                            .setting("led").toLow()
                        .endState()
                        .hasForState("light")
                            .setting("led").toHigh()
                        .endState()
                        .beginTransitionTable()
                            .from("initial").when("button1").isHigh().goTo("button1")
                            .from("initial").when("button2").isHigh().goTo("button2")

                            .from("button1").when("button2").isHigh().goTo("light")

                            .from("button2").when("button1").isHigh().goTo("light")

                            .from("button1").when("button1").isLow().goTo("initial")
                            .from("button2").when("button2").isLow().goTo("initial")

                            .from("light").when("button1").isLow().goTo("button2")
                            .from("light").when("button2").isLow().goTo("button1")
                        .endTransitionTable()
                .build();*/


        // SCENARIO 3
        // Pushing the  button once switch the system in a mode where the LED is switched on. Pushing it again switches it off.
        /*App myApp =
                application("red_button")
                        .uses(sensor("button", 9))
                        .uses(actuator("led", 12))
                        .hasForState("initial").initial()
                            .setting("led").toLow()
                        .endState()
                        .hasForState("led")
                            .setting("led").toHigh()
                        .endState()
                        .beginTransitionTable()
                            .from("initial").when("button").isHigh().goTo("led")
                            .from("initial").when("button").isLow().goTo("initial")
                        .endTransitionTable()
                .build();*/


        // SCENARIO 4
        /*
        App myApp =
                application("red_button")
                        .uses(sensor("button", 9))
                        .uses(actuator("buzzer", 11))
                        .uses(actuator("led", 12))
                        .hasForState("initial").initial()
                            .setting("led").toLow()
                            .setting("buzzer").toLow()
                        .endState()
                        .hasForState("buzzer")
                            .setting("buzzer").toHigh()
                        .endState()
                        .hasForState("led")
                            .setting("buzzer").toLow()
                            .setting("led").toHigh()
                        .endState()
                        .beginTransitionTable()
                        .from("initial").when("button").isHigh().goTo("buzzer")
                        .from("buzzer").when("button").isLow().goTo("led")
                        .from("led").when("button").isLow().goTo("initial")
                        .endTransitionTable()
                        .build();
                        */

        App myApp =
                application("red_button")
                        .uses(sensor("button", 9))
                        .uses(actuator("buzzer", 11))
                        .uses(actuator("led", 12))
                        .hasForState("initial").initial()
                        .setting("led").toLow()
                        .setting("buzzer").toLow()
                        .endState()
                        .hasForState("buzzer")
                        .setting("buzzer").toHigh()
                        .endState()
                        .hasForState("led")
                        .setting("buzzer").toLow()
                        .setting("led").toHigh()
                        .endState()
                        .beginTransitionTable()
                        .from("initial").when("button").isHigh().goTo("buzzer")
                        .from("initial").after(2000).goTo("buzzer")
                        .from("buzzer").when("button").isHigh().goTo("led")
                        .from("led").when("button").isHigh().goTo("initial")
                        .endTransitionTable()
                        .build();

        Visitor codeGenerator = new ToWiring();
        myApp.accept(codeGenerator);
        System.out.println(codeGenerator.getResult());
    }

}
