import json, os, subprocess, sys, tempfile, unittest

HOOK = os.path.join(os.path.dirname(__file__), "..", "hooks", "now_hook.py")


def run(mode, cfg, cwd, **extra):
    payload = dict(cwd=cwd, session_id="s1", **extra)
    env = dict(os.environ, CLAUDE_CONFIG_DIR=cfg)
    out = subprocess.run([sys.executable, HOOK, mode], input=json.dumps(payload),
                         capture_output=True, text=True, env=env, check=True)
    return out.stdout


class NowHookTest(unittest.TestCase):
    def setUp(self):
        self.cfg = tempfile.mkdtemp()
        self.cwd = "/work/api"
        self.state = os.path.join(self.cfg, "state", "-work-api")

    def test_without_now_md_nothing_is_written_or_asked(self):
        run("mark", self.cfg, self.cwd, tool_input={"file_path": "/work/api/x.php"})
        self.assertEqual(run("check", self.cfg, self.cwd), "")
        self.assertFalse(os.path.exists(self.state))

    def test_stale_now_md_blocks_the_stop_once(self):
        os.makedirs(self.state)
        now_md = os.path.join(self.state, "NOW.md")
        open(now_md, "w").write("# api\n")
        os.utime(now_md, (0, 0))
        run("mark", self.cfg, self.cwd, tool_input={"file_path": "/work/api/x.php"})
        self.assertIn('"block"', run("check", self.cfg, self.cwd))
        self.assertEqual(run("check", self.cfg, self.cwd), "")


if __name__ == "__main__":
    unittest.main()
