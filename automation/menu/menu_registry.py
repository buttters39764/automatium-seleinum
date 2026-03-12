from automation.actions.ivi_tarolo import IVITaroloAction
from automation.actions.not_implemented import NotImplementedAction

ACTIONS = [
    IVITaroloAction(),                    # 1
    NotImplementedAction("2", "ÁFE"),     # 2
    NotImplementedAction("3", "V2"),      # 3
]