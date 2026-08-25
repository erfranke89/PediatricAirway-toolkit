import re
import unittest
from pathlib import Path


HTML = (Path(__file__).parents[1] / "index.html").read_text()


class SiteSmokeTests(unittest.TestCase):
    def test_mobile_zoom_is_not_disabled(self):
        viewport = re.search(r'<meta name="viewport" content="([^"]+)"', HTML).group(1)
        self.assertNotIn("maximum-scale", viewport)
        self.assertNotIn("user-scalable=no", viewport)

    def test_all_sections_have_jump_targets(self):
        tabs = set(re.findall(r'data-tab="([^"]+)"', HTML))
        options = set(re.findall(r'<option value="([^"]+)"', HTML))
        self.assertEqual(tabs, options)
        for tab in tabs:
            self.assertIn(f'id="tab-{tab}"', HTML)

    def test_bradycardia_output_cannot_reverse_a_range(self):
        calculation = re.search(r'S\("atrop-brady",(.*?)\);', HTML).group(1)
        self.assertIn('R(', calculation)
        self.assertNotIn('Rr(', calculation)

    def test_accessible_controls_and_direct_links_are_initialized(self):
        self.assertIn('<button class="nav-tab', HTML)
        self.assertIn('aria-expanded', HTML)
        self.assertIn('location.hash.slice(1)', HTML)


if __name__ == "__main__":
    unittest.main()
