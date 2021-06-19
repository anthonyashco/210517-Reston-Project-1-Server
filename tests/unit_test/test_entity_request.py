from entities.request import Request


def test_comments():
    request = Request()
    request.add_comment(0, "Cute Raichu NFT")
    request.add_comment(1, "This is not a responsible use of company funds.")
    assert len(request.request_details) == 2
    assert request.read_comments()[0][1] == "Cute Raichu NFT"
