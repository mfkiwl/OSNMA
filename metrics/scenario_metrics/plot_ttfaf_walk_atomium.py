from pathlib import Path
import sys
OSNMALIB_PATH = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(OSNMALIB_PATH))

import matplotlib.pyplot as plt
import numpy as np

from metrics.metrics_auxiliar.run_and_extract import get_ttfaf_matrixSBF, normal_run_and_exit
from metrics.metrics_auxiliar.predefined_plots import plot_ttfaf, plot_cdf, plot_per_subframe, print_pki
# 2291 39804 -> 03/12/2023 - 11:03:24 UTC
# 2291 42233 -> 03/12/2023 - 11:43:53 UTC

DATA_FOLDER = OSNMALIB_PATH / 'metrics/scenarios/walk_atomium/'

sim_params = {
    "WN": 1267,
    "TOW_START": 39804,
    "TOW_STOP": 42233,
    "name": "Hot Start TTFAF - Walk in Atomium",
    "numpy_file_name": DATA_FOLDER / "ttfaf_matrix_walk_atomium_all.npy",
    "config_dict": {
        'scenario_path': DATA_FOLDER / 'walk_atomium_inav.sbf',
        'exec_path': DATA_FOLDER,
        'pubk_name': 'OSNMA_PublicKey.xml',
        'kroot_name': 'OSNMA_start_KROOT.txt',
        'stop_at_faf': True,
        'log_console': False,
        'log_file': False
    }
}

if __name__ == "__main__":

    # normal_run_and_exit(sim_params)

    options = {
        "IOD SotA. TL 30s": {
            'do_mack_partial_extraction': False, 'do_tesla_key_regen': False, 'do_cop_link_optimization': False,
            'do_dual_frequency': False, 'do_reed_solomon_recovery': False, 'TL': 30
        },
        "IOD SotA. Page proc. TL 25s": {
            'do_mack_partial_extraction': True, 'do_tesla_key_regen': True, 'do_cop_link_optimization': False,
            'do_dual_frequency': False, 'do_reed_solomon_recovery': False, 'TL': 25
        },
        "COP-IOD. Page proc. TL 17s": {
            'do_mack_partial_extraction': True, 'do_tesla_key_regen': True, 'do_cop_link_optimization': True,
            'do_dual_frequency': False, 'do_reed_solomon_recovery': False, 'TL': 17
        },
        "COP-IOD. Page proc. RS. TL 17s": {
            'do_mack_partial_extraction': True, 'do_tesla_key_regen': True, 'do_cop_link_optimization': True,
            'do_dual_frequency': False, 'do_reed_solomon_recovery': True, 'TL': 17
        },
        "COP-IOD. Page proc. Dual-Freq. TL 17s": {
            'do_mack_partial_extraction': True, 'do_tesla_key_regen': True, 'do_cop_link_optimization': True,
            'do_dual_frequency': True, 'do_reed_solomon_recovery': False, 'TL': 17
        },
        "COP-IOD. Page proc. Dual-Freq. RS. TL 17s": {
            'do_mack_partial_extraction': True, 'do_tesla_key_regen': True, 'do_cop_link_optimization': True,
            'do_dual_frequency': True, 'do_reed_solomon_recovery': True, 'TL': 17
        },
    }

    # Rerun from scratch (will take a while) or load the saved matrix
    #ttfaf_matrix = get_ttfaf_matrixSBF(sim_params, options, True)
    ttfaf_matrix = np.load(sim_params["numpy_file_name"])

    plot_ttfaf(ttfaf_matrix, options.keys(), sim_params["name"], DATA_FOLDER)
    plot_per_subframe(ttfaf_matrix, options.keys(), sim_params["name"], DATA_FOLDER)
    plot_cdf(ttfaf_matrix, options.keys(), sim_params["name"], DATA_FOLDER)
    print_pki(ttfaf_matrix, options.keys(), sim_params["name"], DATA_FOLDER)

    plt.show()
