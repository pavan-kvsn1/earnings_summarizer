import unittest
from llm_parser import split_into_sections

class TestSplitIntoSections(unittest.TestCase):

    def test_split_with_known_headers(self):
        report_text = """
This is the introduction.
Financial Results
This is the financial results section.
Revenue was $100 million.
Management Discussion
This section discusses management's view.
Outlook
Future looks bright.
Q&A
Q: What is the capital expenditure?
A: $10 million.
        """
        expected_sections = [
            "This is the introduction.",
            "Financial Results\nThis is the financial results section.\nRevenue was $100 million.",
            "Management Discussion\nThis section discusses management's view.",
            "Outlook\nFuture looks bright.",
            "Q&A\nQ: What is the capital expenditure?\nA: $10 million."
        ]
        self.assertEqual(split_into_sections(report_text), expected_sections)

    def test_no_headers_found(self):
        report_text = "This is a report with no specific section headers. Just a plain text."
        expected_sections = [report_text]
        self.assertEqual(split_into_sections(report_text), expected_sections)

    def test_case_insensitive_headers(self):
        report_text = """
Introduction.
financial results
Details about financials.
MANAGEMENT DISCUSSION
Management's perspective.
outlook
Guidance for next quarter.
        """
        expected_sections = [
            "Introduction.",
            "financial results\nDetails about financials.",
            "MANAGEMENT DISCUSSION\nManagement's perspective.",
            "outlook\nGuidance for next quarter."
        ]
        self.assertEqual(split_into_sections(report_text), expected_sections)

    def test_empty_text(self):
        report_text = ""
        expected_sections = [] # Expecting an empty list for empty input if it contains nothing
        self.assertEqual(split_into_sections(report_text), expected_sections)

    def test_text_with_only_whitespace(self):
        report_text = "   \n   \t   "
        expected_sections = [] # Expecting an empty list for whitespace only input
        self.assertEqual(split_into_sections(report_text), expected_sections)

    def test_sequential_headers(self):
        report_text = """
Financial Results
Outlook
This is the outlook section after a sequential header.
        """
        expected_sections = [
            "Financial Results", # Section 1 is just the header
            "Outlook\nThis is the outlook section after a sequential header." # Section 2
        ]
        self.assertEqual(split_into_sections(report_text), expected_sections)

    def test_text_ending_with_header(self):
        report_text = """
Some initial text.
Financial Results
This is the financial results section.
Outlook
        """
        expected_sections = [
            "Some initial text.",
            "Financial Results\nThis is the financial results section.",
            "Outlook"
        ]
        self.assertEqual(split_into_sections(report_text), expected_sections)

    def test_header_not_at_start_of_line(self):
        report_text = "This is not a header: Financial Results"
        expected_sections = [report_text]
        self.assertEqual(split_into_sections(report_text), expected_sections)

    def test_text_with_only_headers(self):
        report_text = """
Financial Results
Management Discussion
Outlook
        """
        expected_sections = [
            "Financial Results",
            "Management Discussion",
            "Outlook"
        ]
        self.assertEqual(split_into_sections(report_text), expected_sections)

    def test_headers_with_leading_trailing_spaces(self):
        report_text = """
  Financial Results
This is the financial results section.
 Management Discussion
This is the management discussion.
        """
        expected_sections = [
            "  Financial Results  \nThis is the financial results section.",
            " Management Discussion     \nThis is the management discussion."
        ]
        self.assertEqual(split_into_sections(report_text), expected_sections)

if __name__ == '__main__':
    unittest.main()
