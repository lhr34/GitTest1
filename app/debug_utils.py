# app/debug_utils.py
def reset_simulation(data_provider):
    """
    Reset the simulation by clearing the data history.
    """
    data_provider.data_history.clear()
