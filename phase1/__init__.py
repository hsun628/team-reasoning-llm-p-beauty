# models

from otree.api import *
from settings import debug
from settings import num_participant

class C(BaseConstants):
    NAME_IN_URL = 'phase1'
    PLAYERS_PER_GROUP = 4 if debug else num_participant # wait for all 12 participants
    NUM_ROUNDS = 1 if debug else 3
    Correct_Prediction = ["A", "B", "Tie"] # predefined correct predictions (may be randomized)
    Prediction_Reward = 50

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

def calculate_results(self):
    correct_prediction = C.Correct_Prediction[self.round_number - 1]

    for p in self.get_players():
        if p.prediction == correct_prediction:
            p.payoff = cu(C.Prediction_Reward)
        else:
            p.payoff = cu(0)
    
class Player(BasePlayer):  
    prediction = models.StringField(
        choices = ["A", "Tie", "B"],
    )


#############################################################################

# pages

from otree.api import *

class welcome(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    
class Phase1StartWaitPage(WaitPage):
    title_text = "請等待其他受試者完成準備"

    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Prediction(Page):
    form_model = 'player'
    form_fields = ['prediction']

class PredictionWaitPage(WaitPage):
    title_text = "請等待其他受試者完成預測"
    
    after_all_players_arrive = 'calculate_results'

class Results(Page):
    pass

class ResultsWaitPage(WaitPage):
    title_text = "請等待其他受試者確認結果"

page_sequence = [
    welcome,
    Phase1StartWaitPage,
    Prediction,
    PredictionWaitPage,
    Results,
    ResultsWaitPage
]
