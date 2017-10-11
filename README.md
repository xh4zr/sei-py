# sei_py
A Caveon SEI helper library

## Install
```python
pip install sei_py
```

## Include the library
```python
import sei_py
```

## Create the client
### Option 1
```python
client = sei_py.sei.create_client_with_integration(token=<INTEGRATION_TOKEN>, secret=<INTEGRATION_SECRET>, exam_id=<SEI_EXAM_ID>)
exam = client.exam.get()
```

### Option 2
```python
client = sei_py.sei.create_client(username=<SEI_ID>, password=<SEI_SECRET>, exam_id=<SEI_EXAM_ID>)
exam = client.exam.get()
```

### Option 3
DON'T CHOOSE THIS OPTION
IT WILL BE REMOVED
```python
client = sei_py.create_client_with_context(<SEI_ID>, <SEI_SECRET>, <SEI_EXAM_ID>, <SEI_ROLE_SECRET>)
exam = client.exam.get()
```

## Make any request
```python
client = sei_py.sei.create_client_with_integration(token=<INTEGRATION_TOKEN>, secret=<INTEGRATION_SECRET>, exam_id=<SEI_EXAM_ID>)
exam = client.make_request(method='GET', url='/exams/{exam_id}'.format(exam_id=<SEI_EXAM_ID>))
```
