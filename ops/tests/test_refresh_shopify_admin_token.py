import datetime as dt
import io
import json
import pathlib
import sys
import tempfile
import unittest
import urllib.error

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import refresh_shopify_admin_token as rt  # noqa: E402

APP = {"store_domain": "example-shop.myshopify.com", "client_id": "cid", "client_secret": "csecret"}
TOKEN = "shpca_" + "a" * 32


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def opener_returning(payload, calls=None):
    def opener(req, timeout=30):
        if calls is not None:
            calls.append(req)
        return FakeResponse(json.dumps(payload).encode())
    return opener


class ExchangeTests(unittest.TestCase):
    def test_posts_client_credentials_and_computes_expiry_from_start(self):
        calls, start = [], dt.datetime(2026, 9, 26, 20, 0, tzinfo=dt.timezone.utc)
        token, scope, expires = rt.exchange(APP, opener_returning(
            {"access_token": TOKEN, "scope": "read_products,write_products", "expires_in": 86399}, calls), now=start)
        self.assertEqual(token, TOKEN)
        self.assertEqual(scope, "read_products,write_products")
        self.assertEqual(expires, start + dt.timedelta(seconds=86399))
        self.assertEqual(calls[0].full_url, "https://example-shop.myshopify.com/admin/oauth/access_token")
        self.assertIn(b"grant_type=client_credentials", calls[0].data)

    def test_rejects_missing_token_and_bad_expiry(self):
        with self.assertRaises(rt.TokenError):
            rt.exchange(APP, opener_returning({"expires_in": 86399}))
        with self.assertRaises(rt.TokenError):
            rt.exchange(APP, opener_returning({"access_token": TOKEN, "expires_in": 5}))

    def test_http_error_message_does_not_leak_secret(self):
        def opener(req, timeout=30):
            raise urllib.error.HTTPError(req.full_url, 401, "Unauthorized", {}, io.BytesIO(b"csecret"))
        with self.assertRaises(rt.TokenError) as ctx:
            rt.exchange(APP, opener)
        self.assertNotIn("csecret", str(ctx.exception))
        self.assertIn("401", str(ctx.exception))


class StoreTests(unittest.TestCase):
    def test_updates_all_three_files_and_keeps_other_env_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = pathlib.Path(tmp)
            admin, helper, env = d / "admin.json", d / "helper.json", d / "admin.env"
            admin.write_text(json.dumps({"store_domain": APP["store_domain"], "access_token": "old", "app_name": "Legacy"}))
            env.write_text("export SHOPIFY_STORE_DOMAIN=x\nexport SHOPIFY_ADMIN_ACCESS_TOKEN=old\nexport SHOPIFY_API_KEY=k\n")
            expires = dt.datetime(2026, 9, 27, 20, 0, tzinfo=dt.timezone.utc)
            rt.store(TOKEN, "read_products", expires, APP, admin, helper, env)
            a = json.loads(admin.read_text())
            self.assertEqual(a["access_token"], TOKEN)
            self.assertEqual(a["app_name"], "Legacy")
            self.assertEqual(a["expires_at"], expires.isoformat())
            self.assertEqual(json.loads(helper.read_text()), {"access_token": TOKEN})
            lines = env.read_text().splitlines()
            self.assertIn(f"export SHOPIFY_ADMIN_ACCESS_TOKEN={TOKEN}", lines)
            self.assertIn("export SHOPIFY_API_KEY=k", lines)
            self.assertEqual(sum("SHOPIFY_ADMIN_ACCESS_TOKEN" in l for l in lines), 1)
            for f in (admin, helper, env):
                self.assertEqual(f.stat().st_mode & 0o777, 0o600)

    def test_load_app_rejects_non_myshopify_domain(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = pathlib.Path(tmp) / "app.json"
            p.write_text(json.dumps({**APP, "store_domain": "www.dresslikemommy.com"}))
            with self.assertRaises(rt.TokenError):
                rt.load_app(p)


if __name__ == "__main__":
    unittest.main()
