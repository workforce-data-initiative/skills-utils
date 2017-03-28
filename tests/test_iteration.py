from skills_utils.iteration import Batch


def test_Batch():
    iterable = range(100)
    batches = Batch(iterable, 30)
    num_batches = 0
    final = []
    for batch in batches:
        num_batches += 1
        for row in batch:
            final.append(row)

    assert num_batches == 4
    assert len(final) == 100
    assert final == list(range(100))
