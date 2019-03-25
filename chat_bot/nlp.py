from deeppavlov.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.agents.default_agent.default_agent import DefaultAgent
from deeppavlov.agents.processors.highest_confidence_selector import HighestConfidenceSelector


alice_help = PatternMatchingSkill(responses=['help'], patterns=["помощь", "что ты уметь", "кто ты"])
get_current_locaion = PatternMatchingSkill(['where'], patterns=["где я", "моё местоположение"])
return_back = PatternMatchingSkill(['go_back'], patterns=["перейти назад", "вернуться назад"])
fallback = PatternMatchingSkill(['unknown'])

test_bot = DefaultAgent([alice_help, get_current_locaion, return_back, fallback],
                        skills_selector=HighestConfidenceSelector())
