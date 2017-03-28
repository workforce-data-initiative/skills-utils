import logging


class JobPostingImportBase(object):
    def __init__(self, partner_id, s3_conn=None):
        self.partner_id = partner_id
        self.s3_conn = s3_conn

    def postings(self, quarter):
        logging.info('Finding postings for %s', quarter)
        for posting in self._iter_postings(quarter):
            transformed = self._transform(posting)
            transformed['id'] = '{}_{}'.format(
                self.partner_id,
                self._id(posting)
            )
            yield transformed

    def _id(self, document):
        pass

    def _iter_postings(self, quarter):
        pass

    def _transform(self, document):
        pass
