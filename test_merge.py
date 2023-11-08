import unittest
from merge import MergeRequest

class TestMergeRequest(unittest.TestCase):
    def setUp(self):
        self.mr = MergeRequest()

    def test_close_approved(self):
        self.mr.record_vote("Alice", "upvote")
        self.mr.record_vote("Bob", "upvote")
        self.assertEqual(self.mr.close(), "Merge request has been approved and closed")
        self.assertEqual(self.mr.get_status(), MergeRequest.CLOSED)

    def test_close_rejected(self):
        self.mr.record_vote("Alice", "downvote")
        self.mr.record_vote("Bob", "downvote")
        self.assertEqual(self.mr.close(), "Merge request has been rejected and closed")
        self.assertEqual(self.mr.get_status(), MergeRequest.CLOSED)

    def test_close_pending(self):
        self.assertEqual(
            self.mr.close(),
            "Cannot close merge request until it has been approved or rejected",
        )
        self.assertEqual(self.mr.get_status(), MergeRequest.PENDING)

    def test_getvotes_no_votes(self):
        self.assertEqual(self.mr.get_vote_summary(), "No votes yet")

    def test_getvotes_only_upvotes(self):
        self.mr.record_vote("Alice", "upvote")
        self.assertEqual(self.mr.get_vote_summary(), "1 upvotes")

    def test_getvotes_only_downvotes(self):
        self.mr.record_vote("Alice", "downvote")
        self.assertEqual(self.mr.get_vote_summary(), "1 downvotes")

    def test_getvotes_upvotes_and_downvotes(self):
        self.mr.record_vote("Alice", "upvote")
        self.mr.record_vote("Bob", "downvote")
        self.assertEqual(self.mr.get_vote_summary(), "1 upvotes, 1 downvotes")

    def test_vote_upvote(self):
        self.assertEqual(self.mr.record_vote("Alice", "upvote"), None)
        self.assertEqual(self.mr.get_status(), MergeRequest.PENDING)
        self.assertEqual(self.mr.record_vote("Bob", "upvote"), None)
        self.assertEqual(self.mr.get_status(), MergeRequest.APPROVED)

    def test_vote_downvote(self):
        self.assertEqual(self.mr.record_vote("Alice", "downvote"), None)
        self.assertEqual(self.mr.get_status(), MergeRequest.REJECTED)

    def test_vote_closed(self):
        self.mr.record_vote("Alice", "upvote")
        self.mr.record_vote("Bob", "upvote")
        self.mr.close()
        self.assertEqual(
            self.mr.record_vote("Alice", "upvote"), "Can't vote on a closed merge request"
        )

    def test_status_pending(self):
        self.assertEqual(self.mr.get_status(), MergeRequest.PENDING)
        self.mr.record_vote("Alice", "upvote")
        self.assertEqual(self.mr.get_status(), MergeRequest.PENDING)
        self.mr.record_vote("Bob", "downvote")
        self.assertEqual(self.mr.get_status(), MergeRequest.REJECTED)

    def test_status_approved(self):
        self.mr.record_vote("Alice", "upvote")
        self.mr.record_vote("Bob", "upvote")
        self.assertEqual(self.mr.get_status(), MergeRequest.APPROVED)

    def test_status_rejected(self):
        self.mr.record_vote("Alice", "downvote")
        self.mr.record_vote("Bob", "downvote")
        self.assertEqual(self.mr.get_status(), MergeRequest.REJECTED)

if __name__ == "__main__":
    unittest.main()
