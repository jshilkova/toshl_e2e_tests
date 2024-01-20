import logging


def abs_path_from_project(relative_path: str):
    import toshl_finance_demo
    from pathlib import Path

    return (Path(toshl_finance_demo.__file__).parent.parent / relative_path).absolute()

