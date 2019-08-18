import random

from dynamic_stack_decider.abstract_stack_element import AbstractStackElement
from dynamic_stack_decider.abstract_action_element import AbstractActionElement


class SelectorElement(AbstractStackElement):
    """
    A selector element contains multiple action elements.
    The selector element excutes one anction randomly to accomodate the varying environment when the robot is stuck. ~TAT~
    One of the actions will be chosen to execute. Then the action is cached 'as' the 'only' action of the selector element. It means that the selector element will act like the acton element chosen.
    This is not an abstract class to inherit from.
    For clarity, just use ';' to denote selector node while ',' is for sequence node
    """

    ##
    # @Synopsis  pass shared blackboard and dsd to the newly created element
    #
    # @Param blackboard: shared blackboard
    # @Param dsd: shared dynamic stack decider
    # @Param actions: list of initialized action elements
    #
    # @Returns   None
    def __init__(self, blackboard, dsd, actions=()):
        super(SelectorElement, self).__init__(blackboard, dsd)
        self.actions = actions # TODO: whethter to cache the actions?
        index = random.randint(0, len(self.actions)-1)
        self.chosen_action = self.actions[index]

    ##
    # @Synopsis  perform
    #
    # @Param reevaluate: whether the element need to be reevaluated or not. Default is set to 'False'.
    #
    # @Returns   None
    def perform(self, reevaluate=False):
        self.chosen_action.perform()
    
    ##
    # @Synopsis  Represent this stack element as dictionary which is JSON encodable
    #
    # @Returns   a dict
    def repr_dict(self):
        self.publish_debug_data('Active Element', self.chosen_action.__class__.__name__)
        if self.chosen_action._debug_data:
            self.publish_debug_data('Corresponding debug data', self.chosen_action._debug_data)
        data = {
            'type': 'selector',
            'chosen': self.chosen_action.__class__.__name__,
            'content': self.chosen_action.repr_dict(),
            'debug_data': self._debug_data
        }
        self.clear_debug_data()
        return data

