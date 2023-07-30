import os
import pandas as pd
import json
import ast
import matplotlib.pyplot as plt
from typing import Any, Dict

from datetime import datetime

TASKS = {
    "CsLevel.Lowgravity56.VT x WHJ.RWFAP2": '1_strafe_track',
    "CsLevel.Lowgravity56.VT Adjus.ROJF3J": '2_adjust_track',
    "CsLevel.Lowgravity56.VT Berry.RUPVB5": '3_static_entry',
    "CsLevel.Lowgravity56.VT x WHJ.RWIM32": '4_wide_pokeball',
    "CsLevel.Lowgravity56.VT x WHJ.RWFFD8": '5_close_pokeball',
    "CsLevel.VT Empyrean.VT 1w4ts.R1WXON":  '6_1w4ts_clusters',
    "CsLevel.Lowgravity56.VT Angle.RVQZXH": '7_dynamic_micro',
    "CsLevel.Lowgravity56.VT x WHJ.RWFGTB": '8_two_pressure',
}

COLS = ('taskId', 'taskName', 'score', 'mode', 'performance',
        'startedAt', 'endedAt')


def aimlabs_task_data_to_dfs(task_data: list[dict[str, Any]], chosen_tasks: dict[str, str]=TASKS):
    # process data
    data_dict = {key: [] for key in COLS}

    task_data = [datum for datum in task_data 
                 if datum['taskName'] in chosen_tasks]
    for task in task_data:
        for key in COLS:
            value = task[key]
            if value in chosen_tasks:
                value = chosen_tasks[value]
            if key in ('startedAt', 'endedAt'):
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

            data_dict[key].append(value)

    data_df = pd.DataFrame(data_dict)

    # separate performance data
    perf_dict = {}
    perf_dict['taskId'] = data_dict['taskId']
    perf_keys = ast.literal_eval(data_dict['performance'][0]).keys()
    for key in perf_keys:
        perf_dict[key] = []

    for perf in data_dict['performance']:
        perf_info = ast.literal_eval(perf)
        for k, v in perf_info.items():
            perf_dict[k].append(v)

    perf_df = pd.DataFrame(perf_dict)

    return data_df, perf_df
