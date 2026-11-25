"""GUY tiktok companion: offline request preparation only.

Run python companion.py --test for synthetic self-tests.
No network, credentials, publishing, spending or account access.
"""
import argparse
import json
import unittest
from uuid import UUID, uuid4

COMPONENT = "tiktok"
ACTIONS = frozenset(["analytics_read","content_draft","publish_proposal"])


def prepare(action: str, request_id: str | None = None) -> dict:
    if action not in ACTIONS:
        raise ValueError("Unsupported action")
    identifier = str(uuid4()) if request_id is None else request_id
    if str(UUID(identifier)) != identifier:
        raise ValueError("Canonical request identifier required")
    return {"version": "1", "component": COMPONENT,
            "action": action, "request_id": identifier}


class ContractTests(unittest.TestCase):
    def test_supported_actions(self):
        for action in ACTIONS:
            request = prepare(action)
            self.assertEqual(set(request), {"version", "component", "action", "request_id"})
            self.assertEqual(request["component"], COMPONENT)
            self.assertEqual(request["version"], "1")
            self.assertEqual(request["action"], action)
            self.assertEqual(str(UUID(request["request_id"])), request["request_id"])

    def test_reject_unknown(self):
        for action in ("execute", "spend", "publish", "login_password", "fake_engagement"):
            with self.assertRaises(ValueError):
                prepare(action)

    def test_reject_invalid_identifier(self):
        with self.assertRaises(ValueError):
            prepare(sorted(ACTIONS)[0], "bad-id")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--action", choices=sorted(ACTIONS))
    args = parser.parse_args()
    if args.test:
        unittest.main(argv=["companion.py"])
    elif args.action:
        print(json.dumps(prepare(args.action), indent=2))
    else:
        parser.print_help()
