def cast_hexagram(*args, **kwargs):
    from .cli import cast_hexagram as _cast
    return _cast(*args, **kwargs)

try:
    from .case_tracker import (
        init_db,
        add_case,
        add_prediction,
        verify_prediction,
        get_case,
        list_cases,
        get_accuracy_report,
        get_unverified_predictions,
    )
except (ImportError, ValueError):
    from case_tracker import (
        init_db,
        add_case,
        add_prediction,
        verify_prediction,
        get_case,
        list_cases,
        get_accuracy_report,
        get_unverified_predictions,
    )

