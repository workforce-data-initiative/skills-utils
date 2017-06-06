from skills_utils.testing import ImporterTest
from skills_utils import JobPostingImportBase
from unittest.mock import MagicMock, call


class PopulatedImporter(JobPostingImportBase):
    """A basic importer that can be run through the ImporterTest"""
    def _iter_postings(self, quarter):
        return [
            {'one': 'two'},
            {'one': 'four'},
        ]

    def _transform(self, document):
        transformed = {'title': document['one']}
        return transformed

    def _id(self, document):
        return document['one']


def test_tracker():
    """Ensure that the tracker is called"""
    importer = PopulatedImporter(partner_id='xx')
    tracker = MagicMock()
    postings = importer.postings('2015Q1', stats_counter=tracker)
    assert list(postings) == [
        {'id': 'xx_two', 'title': 'two'},
        {'id': 'xx_four', 'title': 'four'}
    ]
    tracker.track.assert_has_calls([
        call(input_document={'one': 'two'}, output_document={'id': 'xx_two', 'title': 'two'}),
        call(input_document={'one': 'four'}, output_document={'id': 'xx_four', 'title': 'four'}),
    ])
