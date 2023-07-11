class HaliteError(Exception):
    pass


class WorkflowFailedToStartError(HaliteError):
    pass


class WorkflowRunNotFoundError(HaliteError):
    pass


class TooManyPlayersError(HaliteError):
    pass


class TooFewPlayersError(HaliteError):
    pass
