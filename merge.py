class MergeRequest:
    """
    Represents a merge request that can be voted on by users.

    The `MergeRequest` object keeps track of the number of upvotes and downvotes
    for the merge request, as well as its status (open or closed).

    Attributes:
        votes (dict): A dictionary that stores the number of upvotes and downvotes
            for the merge request.
        status (str): A string that represents the status of the merge request.

    Methods:
        get_status(): Returns the status of the merge request based on the number of
            upvotes and downvotes.
        record_vote(by_user, vote_type): Records a vote by a user (either an upvote or downvote)
            for the merge request.
    """

    OPEN = "open"
    CLOSED = "closed"
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"

    def __init__(self):
        self.votes = {"upvotes": set(), "downvotes": set()}
        self.status = MergeRequest.OPEN

    def get_status(self):
        if self.status == MergeRequest.CLOSED:
            return self.status
        if self.votes["downvotes"]:
            return MergeRequest.REJECTED
        if len(self.votes["upvotes"]) >= 2:
            return MergeRequest.APPROVED
        return MergeRequest.PENDING

    def record_vote(self, by_user, vote_type):
        if self.status == MergeRequest.CLOSED:
            return "Can't vote on a closed merge request"
        if vote_type == "downvote":
            self.votes["upvotes"].discard(by_user)
            self.votes["downvotes"].add(by_user)
        elif vote_type == "upvote":
            self.votes["downvotes"].discard(by_user)
            self.votes["upvotes"].add(by_user)
        else:
            return "Invalid vote type"

    def close(self):
        current_status = self.get_status()
        if current_status == MergeRequest.APPROVED or current_status == MergeRequest.REJECTED:
            self.status = MergeRequest.CLOSED
            return f"Merge request has been {current_status} and closed"
        return "Cannot close merge request until it has been approved or rejected"

    def get_vote_summary(self):
        upvotes = len(self.votes["upvotes"])
        downvotes = len(self.votes["downvotes"])
        if upvotes == 0 and downvotes == 0:
            return "No votes yet"
        elif upvotes == 0:
            return f"{downvotes} downvotes"
        elif downvotes == 0:
            return f"{upvotes} upvotes"
        else:
            return f"{upvotes} upvotes, {downvotes} downvotes"
