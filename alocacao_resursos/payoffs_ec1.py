import numpy as np
import pandas as pd

from xf_model import build_regret_matrix, build_choice_criteria_matrix, build_normalized_choice_criteria_matrix
from xr_models import evaluate_on_xr_model

payoff_ob1_vpl = np.array([
        [4791.51 ,4732.74],
        [4769.46 ,4713.26],
        [4900.36 ,4839.31],
        [4892.69 ,4816.45],
        [4880.84 ,4781.12],
        [4878.31 ,4819.83],
        [4762.62 ,4699.49],
        [4863.80 ,4783.20]
    ])

payoff_ob2_cvar = np.array([
        [4664.09 ,4594.92],
        [4639.48 ,4573.23],
        [4772.78 ,4701.65],
        [4779.64 ,4694.74],
        [4781.34 ,4680.04],
        [4748.16 ,4679.91],
        [4639.42 ,4565.59],
        [4754.29 ,4665.14]
    ])


payoff_ob3_rar = np.array([
        [127.42 , 137.82],
        [129.98 , 140.03],
        [127.58 , 137.66],
        [113.05 , 121.71],
        [99.50 , 101.08],
        [130.14 , 139.92],
        [123.20 , 133.90],
        [109.50 , 118.06]
    ])

payoff_ob4_ics = np.array([
        [0.00      ,       0.00   ],
        [143.45    ,       143.45 ],
        [119.91    ,       119.91 ],
        [111.46    ,       111.46 ],
        [94.05     ,       94.05  ],
        [125.14    ,       125.14 ],
        [133.94    ,       133.94 ],
        [116.34    ,       116.34 ]
    ])

list_payoffs = [-payoff_ob1_vpl, -payoff_ob2_cvar, payoff_ob3_rar, -payoff_ob4_ics]
list_regret = []
list_ccm = []
list_nccm = []

for m in list_payoffs:
    regret = build_regret_matrix(m)
    list_regret.append(regret)

    ccn = build_choice_criteria_matrix(m)
    list_ccm.append(ccn)

    ncc = build_normalized_choice_criteria_matrix(ccn)
    list_nccm.append(ncc)

array_nccm = np.array(list_nccm)
min_aggregated = np.min(array_nccm, axis=0)
print("end")

