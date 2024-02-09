if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print("Preprocessing: rows with zero passengers", (data['passenger_count'].isin([0]) | data['trip_distance'].isin([0])).sum())
    print(data.dtypes)
    print(data.columns)
    data.columns = (data.columns
                    .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                    .str.lower()
                )
    print(data.columns)
    return data[(data['passenger_count'] > 0.0) & (data['trip_distance'] > 0.0)]

@test
def test_output(output, *args):
    assert output['passenger_count'].isin([0]).sum() ==0, 'There are rides with zero passengers'
    assert output['trip_distance'].isin([0]).sum() ==0, 'There are rides with zero trip distance'
    assert "vendor_id" in output.columns.tolist(), 'VendorID was not renamed'