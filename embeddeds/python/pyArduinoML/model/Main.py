__author__ = 'pascalpoizat'

"""
DSL version of the demo application
uses MethodChaining, nothing Python-specific
"""


def demo1():
    """
    Direct use of the DSL.
    + : auto-completion (limited due to python typing system)
    - : verbose, Python syntax requires '\' to cut lines.

    :return:
    """
    from pyArduinoML.methodchaining.AppBuilder import AppBuilder
    from pyArduinoML.model.SIGNAL import SIGNAL

    app = AppBuilder("Switch!").sensor("BUTTON").on_pin(9).actuator("LED").on_pin(12) \
        .state("off") \
            .set("LED").to(SIGNAL.LOW) \
            .when("BUTTON").has_value(SIGNAL.HIGH).go_to_state("on") \
        .state("on") \
            .set("LED").to(SIGNAL.HIGH) \
            .when("BUTTON").has_value(SIGNAL.HIGH).go_to_state("off") \
        .get_contents()

    print(app)

if __name__ == '__main__':
    demo1()
